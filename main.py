from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Float


    

#Banco
engine = create_engine("sqlite:///./lojadb", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#Models
class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)

    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="produtos")

Base.metadata.create_all(bind=engine)

#App
app = FastAPI()
templates = Jinja2Templates(directory="templates")

#Home
@app.get("/", response_class=HTMLResponse)
def listar_categorias(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

#Categorias
@app.get("/", response_class=HTMLResponse)
def listar_categorias(request: Request):
    db = SessionLocal()
    categorias = db.query(Categoria).all()
    db.close()
    return templates.TemplateResponse("categorias.html", {
        "request": request,
        "categorias": categorias

    })
@app.post("/categorias")
def criar_categoria(nome: str = Form(None)):
    db = SessionLocal()
    db.add(Categoria(nome=nome, descricao=declarative_base))
    db.commit()
    db.close()
    return RedirectResponse("/categorias", status_code=303)

#Produtos
@app.get("/produtos", response_class=HTMLResponse)
def listar_produtos(request: Request):
    db = SessionLocal()
    produtos = db.query(Produto).all()
    categorias = db.query(Categoria).all()
    db.close()
    return templates.TemplateResponse("produtos.html",{
        "request": request,
        "produtos": produtos,
        "categorias": categorias

    })

@app.post("/produtos")
def criar_produto(nome: str = Form(...), categoria_id: int = Form(...)):
    db = SessionLocal()
    db.add(Produto(nome=Produto, categoria_id=categoria_id)) 
    db.commit()
    db.close()
    return RedirectResponse("/produtos", status_code=303)


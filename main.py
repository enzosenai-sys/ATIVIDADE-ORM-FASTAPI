from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, Column, Integer, String, Foreignkey
from sqlalchemy.orm import sessionmaker

#Banco
engine = create_engine("sqlite:///./lojadb", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#Models
class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    categoria_id = Column(Integer, Foreignkey("categorias.id"))
    categoria = relatioship("Categoria", back_populates="produtos")

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
def criar_categoria(nme: str = Form(...)):
    db = SessionLocal()
    db.add(Categoria(nome=Categoria))
    db.commit()
    db.close()
    return RedirectResponse("/categorias", status_code=303)

#Produtos

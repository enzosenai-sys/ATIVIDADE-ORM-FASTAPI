from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLRespnse, RedirectResponse
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

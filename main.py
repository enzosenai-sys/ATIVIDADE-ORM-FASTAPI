from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLRespnse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, Column, Integer, String, Foreignkey
from sqlalchemy.orm import sessionmaker

#Banco
engine = create_engine("sqlite:///./lojadb", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


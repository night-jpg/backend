#from typing import Optional

from sqlite3.dbapi2 import Cursor
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json
import sqlite3
from pydantic.types import Json
import uvicorn

app = FastAPI()

#Filmes
class Movie(BaseModel): 
    id: int
    title: str
    year: int
    genre: str
    synopsis : str
    rating: float

#Base de dados

conn = sqlite3.connect('movies.db',check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE movies(id int,  data json)")


#Get all
@app.get("/filmes")
def get_All():
    return c.execute("SELECT * FROM movies")

#Post movie
@app.post("/filmes")
def insert_user(movie: Movie):
    c.execute("INSERT INTO movies VALUES (?,?)",[movie.id,json.dumps([movie.title,movie.year,movie.genre,movie.synopsis,movie.rating])])
    conn.commit()
    return "Filme "+movie.title+" adicionado com sucesso"


#Get por id
@app.get("/filmes/{id}")
def get_Movie_By_Id(id_movie: int):
    c.execute("SELECT data from movies WHERE id = (?);",[id_movie])
    return c.fetchall()

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")
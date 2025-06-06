#se ejecuta DENTRO de la carpeta del back uvicorn main:app --reload, pero es para ejecutar la api 


#esta es con fastapi
#aqui se crean dos API con dos endpoints recibir obtener
#usamos pydantic para lo de la validacion en estructuras de datos 
#uvicorn es para la ejecucion de un servidor web
from fastapi import FastAPI 
from pymongo import MongoClient as cliente 
from pydantic import BaseModel 
import uvicorn as servidor

client = cliente("mongodb://localhost:27017/hackathonmovilidad")  
db = client["hackathonmovilidad"]
collection = db["datos"] #en la coleccion se guardan los registros que recibimos desde la API

app = FastAPI()

#esto se anade pero es para permitir solicitudes de donde sea, pero esta en un veremos
app.add_middleware(
    CORSMiddleware, #es para el middleware que usa cors 
    allow_origins=["*"],  #deja solicitudes de cualquier origen
    allow_credentials=True, #para la manejacion de autenticacion en usuarios 
    allow_methods=["*"],  #deja todos los metodos http
)

#pydantic hace que datos enviados a la api puedan ser validados
class inicioDatos(BaseModel):
    #DATOS tieenen que estar en formato JSON
    #se tienen que indicar los datos si vienen de web o de arduido en dict
    origen: str 
    datos: dict 

@app.post("/recibe_datos/")
def recibe_datos(entrada: inicioDatos):
    #entrasa se usa como json que el usuario manda a la api
    nuevos_dato = {
        "origen": entrada.origen,
        "datos": entrada.datos
    }
    resultado = collection.insert_one(nuevos_dato) #se esta guardando en la bd
    return {"mensaje": "Datos guardados", "id": str(resultado.inserted_id)}

@app.get("/obtener_datos/")
def obtener_datos():
    datos = list(collection.find({}, {"_id": False})) #oculta el objid que mongo agrega
    return {"datos": datos}

#se tiene que ejecutar la api con uvicorn
if __name__ == "__main__":
    servidor.run(app, host="127.0.0.1", port=8000)

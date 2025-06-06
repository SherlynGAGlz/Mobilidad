from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn

# Conectar con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mi_base_de_datos"]
collection = db["datos"]

app = FastAPI()

# Modelo de datos
class InputData(BaseModel):
    fuente: str  # "web" o "arduino"
    datos: dict  # Datos de entrada

# Endpoint para recibir datos desde la web o Arduino
@app.post("/recibir_datos/")
def recibir_datos(entrada: InputData):
    # Guardar en la base de datos
    resultado = collection.insert_one(entrada.dict())
    return {"mensaje": "Datos recibidos", "id": str(resultado.inserted_id)}

# Endpoint para obtener datos
@app.get("/obtener_datos/")
def obtener_datos():
    datos = list(collection.find({}, {"_id": 0}))
    return {"datos": datos}

if _name_ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000)
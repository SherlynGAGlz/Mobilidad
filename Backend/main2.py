#esta esta con flask
#al correrlo sale una advertencia es porque el servidor que se está ejecutando es para desarrollo, 
#no es el indicado como  quien dice para un entorno de produccion
#el debugger es por si se necesita interactuar con el depurador en el navegador, es el PIN de seguridad 
from flask import Flask, request, jsonify 
#pide peticioones http
#convierte datos en una respuesta JSON por el navegador o cliente http
from flask_pymongo import PyMongo  as mongo
from flask_cors import CORS  #front acceda a la api
from bson.objectid import ObjectId  #maneja id de MongoDB

app = Flask(__name__) 
CORS(app)  #se permite el acceso al front

app.config["MONGO_URI"] = "mongodb://localhost:27017/hackathonmovilidad2.1"  
mongo = mongo(app) 

@app.route("/")
def inicio():
    return "Esta corriendo con flaskkkk"  

@app.route("/login", methods=["POST"])
def login():
    datos = request.json  #este es para el usuario
    id = datos.get("id")  
    clave = datos.get("password") 

    usuario = mongo.db.usuarios.find_one({"id": id, "password": clave}) 

    if usuario:
        #el 200 es por exitoso, y el 401 es de errores
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200 
    else:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401 

@app.route("/reportes", methods=["POST"])
def agregar_reportes():
    reporte = request.json  
    mongo.db.reportes.insert_one(reporte) 
    return jsonify({"mensaje": "Tarea agregada correctamente"}), 201 

@app.route("/reportes", methods=["GET"])
def obtener_reportes():
    reportes = mongo.db.reportes.find() 
    lista_reportes = [] 
    for reporte in reportes:  
        reporte["_id"] = str(reporte["_id"])  #se pasa a str para formato json
        lista_reportes.append(reporte)  
    return jsonify(lista_reportes), 200  

@app.route("/reportes/<id>", methods=["PUT"])
def editar_reporte(id):
    nueva_info = request.json  
    mongo.db.reportes.update_one({"_id": ObjectId(id)}, {"$set": nueva_info})  
    return jsonify({"mensaje": "Reporte actualizado"}), 200  

@app.route("/reportes/<id>", methods=["DELETE"])
def eliminar_reporte(id):
    mongo.db.reporte.delete_one({"_id": ObjectId(id)}) 
    return jsonify({"mensaje": "Reporte eliminado"}), 200  

#esta es para la IA, pero solo simulaciones
#solo tomar de EJEMPLO
#@app.route("/procesar", methods=["POST"])
#def procesar_ia():
#    resultado = np.random.rand()  
#    return jsonify({"resultado": resultado}), 200  

#se ejecuta para iniciar en modo de depuracion 
if __name__ == "__main__":
    app.run(debug=True)

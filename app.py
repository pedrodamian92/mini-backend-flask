from flask import Flask, request, jsonify
from db import get_connection

# Incializa la aplicacion web; app se covierte en el objeto 
app = Flask(__name__)

# Cuando alguien visite la ruta "/" (pagina principal-raiz) ejecuta la funcion home 
# Tambien con el hecho de ver Running on http://127.0.0.1.5000/(Press CTRL + C to quit)
# Esto no es un endpoint
# Cuando alguien entre a la ruta dispara la funcion 
# Ruta = parte interna /clientes
# Direccion (URL) lo que se escribe en el navegador
# (Endpoint = ruta + metodo HTTP p.e. GET/clientes
@app.route("/")
def home():
    print("Alguien esta visitando la pagina")
    return "Servidor Flask funcionando"

# define un endpoint en la URL /clientes que acepta peticiones
# de tipo POST (crear) 
@app.route('/clientes', methods=['POST']) #tipo POST -> CREAR
def crear_cliente():
    #toma el JSON que envia el cliente  (esto es un diccionario)
    data = request.json

    # Flask acepta formularios HTML
    print("Llego una peticion")
    #nombre = request.form['nombre']
    #email = request.form['email']

    # abre la conexion a la base MySQL usando la funcion db.py
    conexion = get_connection()
    # crea un cursor que permite enviar instrucciones SQL a
    # la base y recibir resultados
    cursor = conexion.cursor()

    # ejecuta el INSERT con los valores recibidos
    cursor.execute(
        "INSERT INTO clientes(nombre, email) VALUES (%s, %s)",
        (data['nombre'], data['email'])
    )

    # guarda los cambios en la base
    conexion.commit()
    # cierra el cursor
    cursor.close()
    # cierra la conexion 
    conexion.close()
    # devuelve un mensaje en formato JSON confirmando la creacion
    # con codigo HTTP 201(creado) 
    return jsonify({"mensaje": "cliente creado"}), 201

# Endpoint para listar clientes (GET)

@app.route('/clientes', methods=['GET'])

# funcion que se ejecuta cuando alguien llama al endpoint
# @pp.route es un decorador
def listar_clientes():
    
    # Abre la conexion a tu base de datos MySQL usando tu funcion get_connection() de db.py
    conexion = get_connection()
    
    # crea un cursor para ejecutar consultas SQL 
    # dictionary=True hace que cada fila se devuelva como un diccionario en lugar de tupla
    cursor = conexion.cursor(dictionary=True)
    
    # Ejecuta la consulta SQL para traer todos los registros de la tabla clientes.
    cursor.execute("SELECT * FROM clientes")
    
    # Recupera o trae todas las filas del resultado y las guarda en la variable clientes
    clientes = cursor.fetchall()

    # Cierra la conexion a la base de datos
    conexion.close()

    # Convierte la lista de diccionarios en JSON y lo devuelve como respuesta HTTP
    # El navegador o cualquier aplicacion verá los datos en formato estandar 
    return jsonify(clientes)

# Definicion del endpoint para registrar los movimientos
# Si quiero crear un movimiento no debo usar el navegador 
# Debes enviar un POST con JSON se puede usar: curl, httpie o un script en Python 
@app.route('/movimientos', methods=['POST'])
def crear_movimientos():
    
    # recibes el JSON con los datos del movimiento
    data = request.json #Flask toma el body JSON que envio el cliente y lo convierte en dict

    # Abre la conexion a la base MySQL usando la funcion db.py
    conexion = get_connection()

    # crea un cursor que permite enviar las instrucciones SQL a la
    # la base y recibir resultados
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO movimientos (id_cliente, monto, tipo) VALUES (%s, %s, %s)",
        (data['id_cliente'], data['monto'], data['tipo'])
    )

    # guarda los cambios en la base 
    conexion.commit()

    # Cierra la conexion a la base de datos 
    conexion.close()
    
    # Confirmas al cliente que el movimiento fue registrado
    return jsonify({"mensaje":"Movimiento registrado"}), 201

#Endpoint para listar todos los movimientos 
@app.route("/movimientos", methods=['GET'])
def listar_movimientos():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(movimientos)
    # En realidad si puedes saber si funciono escribiendo
    # curl http://127.0.0.1:5000/movimientos

# semanticamente dame los movimientos del cliente con este ID
@app.route('/clientes/<int:id>/movimientos', methods = ['GET'])
def movimientos_cliente(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True) # cuando 
    # utilices fetchall devolvera diccionario caso contrario devolvera tuplas
    # es independiente de cursor.execute

    cursor.execute(
        "SELECT * FROM movimientos WHERE id_cliente = %s",
        (id,) 
        # cursor.execute siempre devuelve tuplas por lo que nada mas 
        # se le indica que haga el id 
    )

    movimientos = cursor.fetchall() # Aqui devolvera diccionario ya que se especifico
    # print(movimientos)
    cursor.close()
    conexion.close()
    return jsonify(movimientos)


#Endpoint para eliminar un cliente 
@app.route('/clientes/<int:id>', methods=['DELETE'])
# El methods = ['DELETE'] define el tipo de solicitud que acepta el servidor
# Por eso el cliente tiene que definir el metodo delete
# OJO: el navegador, al escribir una URL en la barra de direcciones
# siempre hace una petición GET(no podras eliminar poniendio un numero al final)
#Funcion que elimina un cliente 
def eliminar_cliente(id):
    #Objeto que establece la conexion con la base de datos
    conexion = get_connection()

    #Objeto cursor que permite enviar las instrucciones a MySQL
    cursor = conexion.cursor()

    #Indicaciones 
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    #Cuando se pasa parametros a .execute se espera lista o 
    # tupla 

    #Guarda los cambios en la base de datos 
    conexion.commit()

    #Cierra la conexion 
    cursor.close()

    #Cierra la conexion 
    conexion.close()

    #Confirma al cliente que un dato fue removido
    return jsonify({"mensaje": f"Cliente {id} eliminado"}), 200

#Endpoint para modificar todos los campos de un registro existente
@app.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    data = request.get_json()
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("UPDATE clientes SET nombre = %s, email = %s WHERE id =%s",
                   (data['nombre'], data['email'], id)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": f"Cliente {id} actualizado"}), 200

# Se asegura de levantar un servidor web 
if __name__ == "__main__":
    app.run(debug=True)

# API conjunto de endpoints que exponen operacioes y datos
# /clientes y /movimientos son endpoints de tu API REST
# cada vez que se define un @app.route() se amplia el API
# API forma estandarizada de hablar con un programa desde otro programa (contrato)
# API es un conjunto de direcciones que aceptan peticiones y devuelven datos
# Flask crea API
# API estilo de diseño para API web

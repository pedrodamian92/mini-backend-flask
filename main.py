""" 
Script que llama a la funcion get_connection() 
para establecer la comunicacion con MySQL,
utilizando el modulo db. 
# Modulo : archivo.py con muchas funciones/ clases (Un martillo)
# Libreria : conjunto de modulos que ofrecen otras funcionalidades (Caja de herramientas)
# Framework : Conjunto mas grande y estructurado de librerias/modulos para trabajar en algo 
(Como un plano , todo un proyecto de construccion, reglas y procesos definidos. Metodo 
de trabajo, que va primero, como se colocan materiales, normas de seguridad)
"""
from db import get_connection

# Ejercicio de establecer conexion con la base de datos y consulta simple
conexion = get_connection() # Esto es un objeto
cursor = conexion.cursor()  # Tambien es un objeto creado para insertar indicaciones

#Minima accion: Consulta de elementos de la tabla clientes. 
cursor.execute("SELECT * FROM clientes") 
resultados = cursor.fetchall() #Devuelve elementos como tuplas 

for fila in resultados:
    print(fila)

cursor.close() #Cierra al objeto y evita fuga de memoria 
conexion.close() #cierra la conexion, no la deja abierta

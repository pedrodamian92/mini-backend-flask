# Importamos la libreria o modulo request 
# Supongo que tiene que ver exclusivamente con peticiones y pruebas y atributos de estos
import requests

url = "http://127.0.0.1:5000/movimientos" # es la ruta donde se establece la conexion con movimientos
data = {"id_cliente":3, "monto":1500, "tipo":"pago"} #Se define en un diccionario
# el id_cliente, monto y tipo(puede ser cargo o pago)
response = requests.post(url, json=data) # variable que obtiene la respuesta devuelta 

print("Codigo de estado", response.status_code) # imprime el atributo del estado de la respuesta
print("Respuesta JSON:", response.json()) # imprime la respuesta json 

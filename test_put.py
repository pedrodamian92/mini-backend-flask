import requests

# URL del endpoint 
url = "http://127.0.0.1:5000/clientes/1"
data = {"nombre":"Damian Mendez", "email": "damiancrazy@example.com"}
response = requests.put(url, json=data)

print("Codigo de estado", response.status_code)
print("Respuesta JSON", response.json())


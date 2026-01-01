import requests

url = "http://127.0.0.1:5000/clientes/2"
response = requests.delete(url)

print("Codigo de estado:", response.status_code)
print("Respuesta JSON:", response.json())


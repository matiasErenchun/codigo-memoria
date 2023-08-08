from datetime import datetime

import requests

date = datetime.now()
print(date)
response = requests.post('http://127.0.0.1:5000/addDetecction', headers={
    'dateDetection': str(date),
    'IdTelegramUser': str(5274207076),
    'urlImagen': 'http://localhost:8001/prueba1.jpg'
})
print(response.json())


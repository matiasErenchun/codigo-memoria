import asyncio
import websockets
import cv2
import numpy as np
from queue import Queue
import threading
import random
from datetime import datetime
import requests


def image_processor(barrier, image_queue):
    barrier.wait()
    while True:
        try:
            # Envía mensajes al servidor
            data = image_queue.get(timeout=5)
            image_data = data['image']
            time_str = data['time']
            randomm = data['random']
            width = data['width']
            height = data['height']
            print("time: " + str(time_str))
            nparr = np.frombuffer(image_data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_np = cv2.resize(img_np, (1920, 1080))

            # mostramos la imagen con OpenCV
            ruta = 'D:\\mm\\Detecciones\\' + str(randomm) + '-' + str(time_str) + '.jpg'
            # Escribe la imagen en un archivo
            cv2.imshow("Imagen recibida", img_np)
            cv2.waitKey(1)
            val = random.randint(1, 100)
            if val < 6:
                try:
                    cv2.imwrite(ruta, img_np)
                    date = datetime.now()
                    print(date)
                    response = requests.post('http://127.0.0.1:5000/addDetecction', headers={
                        'dateDetection': str(date),
                        'IdTelegramUser': str(5274207076),
                        'urlImagen': 'http://localhost:8003/' + str(randomm) + '-' + str(time_str) + '.jpg',
                        'source': 'BirdDetector',
                        'class': 'ave_tierra',
                    })
                except Exception as e:
                    print(e)
                    print("error al guardar o mandar imagen ")
        except Exception:
            print("algo ocurre")
    cv2.destroyAllWindows()


async def websocket_handler(websocket, path, barrier, images_queue):
    # Se ejecuta cuando se establece una conexión websocket
    print("Conexión establecida.")
    barrier.wait()
    try:
        while True:
            # Recibir datos del cliente
            data = await websocket.recv()

            received_data = eval(data)

            print(f"dandom value:{received_data['random']}")
            images_queue.put(received_data)
            # Enviar una respuesta al cliente
            response = "Respuesta del servidor"
            # await websocket.send(response)
            print(f"Respuesta enviada: {response}")

    except websockets.exceptions.ConnectionClosedOK:
        # La conexión websocket se ha cerrado de forma normal
        print("Conexión cerrada.")

    except websockets.exceptions.ConnectionClosedError as e:
        # La conexión websocket se ha cerrado con un error
        print(f"Error al cerrar la conexión: {e}")


images_queue = Queue()
barrier = threading.Barrier(2)
thread = threading.Thread(target=image_processor, args=(barrier, images_queue))
thread.start()
# Crear el servidor websocket
start_server = websockets.serve(
    lambda websocket, path: websocket_handler(websocket, path, barrier, images_queue),
    "localhost",
    8765,
    max_size=2 ** 25
)

# Iniciar el bucle de eventos de asyncio
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
thread.join()

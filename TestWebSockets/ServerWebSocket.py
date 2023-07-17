import asyncio
import websockets
import cv2
import numpy as np


async def websocket_handler(websocket, path):
    # Se ejecuta cuando se establece una conexión websocket
    print("Conexión establecida.")

    try:
        while True:
            # Recibir datos del cliente
            data = await websocket.recv()

            received_data = eval(data)

            print(f"dandom value:{received_data['random']}")
            image_data = received_data['image']
            time_str = received_data['time']
            randomm = received_data['random']
            width = received_data['width']
            height = received_data['height']
            print("time: " + str(time_str))
            nparr = np.frombuffer(image_data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_np = cv2.resize(img_np, (width, height))

            # mostramos la imagen con OpenCV
            ruta = 'imagenes/' + str(randomm) + '-' + str(time_str) + '.jpg'
            # Escribe la imagen en un archivo
            cv2.imwrite(ruta, img_np)

            # Procesar los datos o realizar alguna acción

            # Enviar una respuesta al cliente
            response = "Respuesta del servidor"
            # await websocket.send(response)
            print(f"Respuesta enviada: {response}")

    except websockets.exceptions.ConnectionClosedOK:
        # La conexión websocket se ha cerrado de forma normal
        print("Conexión cerrada de forma normal.")

    except websockets.exceptions.ConnectionClosedError as e:
        # La conexión websocket se ha cerrado con un error
        print(f"Error al cerrar la conexión: {e}")


# Crear el servidor websocket
start_server = websockets.serve(websocket_handler, "localhost", 8765, max_size=2 ** 25)

# Iniciar el bucle de eventos de asyncio
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

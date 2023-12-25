import asyncio
import websockets
import cv2
import os
import datetime
import random
from queue import Queue
import threading
import sys


def contar_camaras():
    num_cameras = 0
    while True:
        try:
            cap = cv2.VideoCapture(num_cameras)
            if not cap.read()[0]:
                break
        except Exception:
            print("si")
            break

        num_cameras += 1
        cap.release()
    print(f"cantidad de camaras detectadas:{num_cameras}")
    return num_cameras


'''
para definir el formato de captura por parte de la camara,
se debe revisar la documentacion tanto de la cama como de opencv:
https://docs.opencv.org/3.3.0/d0/da7/videoio_overview.html
para nuestro caso en windows se recomienda usar DSHOW y para linux v4l2
'''


def get_camera(i):
    if os.name == 'posix':
        print("posix: linux")
        camera = cv2.VideoCapture(i, cv2.CAP_V4L2)
    elif os.name == 'nt':
        print("nt: windows")
        camera = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    else:
        print("otro: sistema desconocido")
        camera = cv2.VideoCapture(i)
    return camera


def resoluciones_disponibles(i):
    cap = get_camera(i)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    # Lista de posibles resoluciones
    resolutions = [(4656, 3496), (3264, 2448), (2592, 1944), (1920, 1080), (1280, 720), (640, 480)]
    mwidth = 640
    mheight = 480
    # Iterar sobre cada resolución y verificar si es posible establecerla
    for res in resolutions:
        width, height = res
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if cap.get(cv2.CAP_PROP_FRAME_WIDTH) == width and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == height:
            print(f"la camara {i} soporta la resolucion: {width} x {height}")
            if width > mwidth and height > mheight:
                mwidth = width
                mheight = height
    # Liberar el objeto de captura de video
    cap.release()
    print(f"max w:{mwidth}, max h:{mheight}")
    return mwidth, mheight


def enqueue_images(camera, width, height, id_camara, cola_mensajes, cola_errores):
    ret, frame = camera.read()
    if ret:
        retval, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()

        # Obtiene la fecha y hora actual
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H%M%S.%f")

        # Combina los datos de la imagen y la hora en un diccionario
        data = {'image': image_data, 'time': time_str, 'random': random.randint(1, 100), 'width': width,
                'height': height}

        cola_mensajes.put(data)
    else:
        data_error = {"camra": id_camara, "error": "no se pudo capturar frame"}
        cola_errores.put(data_error)


def controlador_camar(barrier, id_camara, cola_mensajes, cola_errores, prueba):
    width, height = resoluciones_disponibles(id_camara)
    camera = get_camera(id_camara)
    camera.set(cv2.CAP_PROP_FPS, 10.0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print(f"camara {id_camara}Resolución del frame: {width} x {height}")
    barrier.wait()
    if prueba == True:
        contador = 0
        print("test :D")
        while contador < 10:
            enqueue_images(camera, width, height, id_camara, cola_mensajes, cola_errores)
            contador += 1
        print("Prueba terminada")
    else:
        continuar = True
        while continuar:
            enqueue_images(camera, width, height, id_camara, cola_mensajes, cola_errores)


async def websocket_client(barrier, message_queue, ip, puerto):
    uri = f"ws://{ip}:{puerto}"  # Especifica la dirección del servidor websocket
    print(uri)
    barrier.wait()
    async with websockets.connect(uri, ) as websocket:
        while True:
            try:
                # Envía mensajes al servidor
                data = message_queue.get(timeout=20)
                serialized_data = str(data).encode()
                await websocket.send(serialized_data)
                print(f"Mensaje enviado")

                # Espera la respuesta del servidor
                # response = await websocket.recv()
                # print(f"Respuesta recibida: {response}")
            except Exception:
                print("algo ocurre")
    print("Conexión cerrada.")


def get_parameters():
    # Verificar que se hayan proporcionado suficientes argumentos
    if len(sys.argv) < 4:
        print("Uso: python mi_script.py <ip> <puerto> <modo>")
        sys.exit(1)

    # Obtener los argumentos de línea de comandos
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
    modo = sys.argv[3]

    # Tu lógica de programa aquí
    return ip, puerto, modo


# Iniciar el cliente websocket
if __name__ == '__main__':
    ip, puerto, prueba = get_parameters()
    print(prueba)
    num_children = 1
    if prueba == 'True':
        prueba = True
    else:
        num_children = contar_camaras()
        prueba = False
    print(f"nc:{num_children},p:{prueba}")
    cola_mensajes = Queue()
    cola_errores = Queue()
    barrier = threading.Barrier(num_children + 1)

    capture_threads = []
    for i in range(0, num_children):
        p = capture_threads = []
        thread = threading.Thread(target=controlador_camar, args=(barrier, i, cola_mensajes, cola_errores, prueba))
        capture_threads.append(thread)
        thread.start()
    print(f"procesos iniciados{len(capture_threads)}")
    # ver como funca esta parte.
    asyncio.get_event_loop().run_until_complete(websocket_client(barrier, cola_mensajes, ip, puerto))

    for thread in capture_threads:
        thread.join()

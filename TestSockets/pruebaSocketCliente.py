import socket
import time
import cv2
import datetime
import random
from multiprocessing import Process, Queue
import multiprocessing
import os


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
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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


def controlador_camar(stop_event, id_camara, cola_mensajes, cola_errores):
    time.sleep(1)
    width, height = resoluciones_disponibles(id_camara)
    camera = get_camera(id_camara)
    camera.set(cv2.CAP_PROP_FPS, 10.0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print(f"Resolución del frame: {width} x {height}")
    continuar = True
    i = 0
    while continuar and i < 2:
        ret, frame = camera.read()
        if ret:
            # Codifica la imagen en formato JPEG
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
        i += 1


if __name__ == '__main__':
    # Dirección IP y puerto del servidor
    cola_mensajes = Queue()
    cola_errores = Queue()
    IP = '127.0.0.1'
    PORT = 9999

    IP_ADDRESS = '127.0.0.1'  # Dirección IP del servidor
    PORT = 9999  # Puerto del servidor
    BUFFER_SIZE = 4096  # Tamaño del búfer

    # Crea un socket y conecta al servidor
    capturas = 0
    camras_conectadas = contar_camaras()
    # validar_resoluciones(camras)
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## iniciar los procesos
    stop_event = multiprocessing.Event()

    # Creamos dos procesos hijos
    processs = []
    for i in range(camras_conectadas):
        p = multiprocessing.Process(target=controlador_camar, args=(stop_event, i, cola_mensajes, cola_errores))
        p.start()
        processs.append(p)
    img = cv2.imread('E:\\resposGit\\codigo-memoria\\TestSockets\\imagenes_capturadas\\4-2023-07-02 150414.372084.jpg')
    cv2.imshow('Imagen', img)
    s.connect((IP_ADDRESS, PORT))
    while True:
        key = cv2.waitKey(20)
        if key == ord('q'):  # salimos si se presiona la tecla 'q'
            stop_event.set()
            break
        if cola_mensajes.qsize() > 0:
            try:
                print("si")

                print("se conecto")
                data = cola_mensajes.get()
                # Convierte el diccionario a una cadena de bytes
                serialized_data = str(data).encode()
                size = len(serialized_data)
                size_data = size.to_bytes(4, byteorder='big')
                s.sendall(size_data)
                # Envía los datos a través del socket
                print("mandando")
                offset = 0
                while offset < size:
                    packet = serialized_data[offset:offset + BUFFER_SIZE]
                    s.sendall(packet)
                    offset += len(packet)
                print("se mando")
            # Esperamos 5 segundos antes de detener los procesos
            # esperamos 20 milisegundos a que se presione una tecla
            except Exception as e:
                print("algo ocurrio:")
                print(e)

    for p in processs:
        p.join()
    s.close()
    cv2.destroyAllWindows()

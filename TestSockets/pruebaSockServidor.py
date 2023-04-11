import msvcrt
import socket
import sys
import keyboard
import cv2
import numpy as np
import os
import datetime
import signal
import multiprocessing as mp
import threading
import base64

import select

host_ip = '192.168.1.38'
print('HOST IP:', host_ip)
port = 9999

IP_ADDRESS = '127.0.0.1'  # Dirección IP del servidor
PORT = 9999  # Puerto del servidor
BUFFER_SIZE = 4096  # Tamaño del búfer


def process_image(conn, addr):
    print(f'Conexión aceptada desde {addr[0]}:{addr[1]}')
    while True:
        try:
            # print('Esperando conexión...')
            # Recibe los datos del cliente
            size_data = conn.recv(4)
            size = int.from_bytes(size_data, byteorder='big')

            # Recibir datos de imagen en paquetes
            data = b''
            while len(data) < size:
                packet = conn.recv(BUFFER_SIZE)
                if not packet:
                    break
                data += packet

            # Convierte la cadena de bytes en un diccionario
            serialized_data = data.decode()
            data = eval(serialized_data)

            # Obtiene la imagen y la hora de los datos recibidos
            image_data = data['image']
            time_str = data['time']
            randomm = data['random']
            width = data['width']
            height = data['height']
            print("time: " + str(time_str))
            nparr = np.frombuffer(image_data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_np = cv2.resize(img_np, (width, height))

            # mostramos la imagen con OpenCV
            ruta = 'imagenes_capturadas/' + str(randomm) + '-' + str(time_str) + '.jpg'
            # Escribe la imagen en un archivo
            cv2.imwrite(ruta, img_np)
            # with open(ruta, 'wb') as f:
            #   f.write(image_data)

            # Convierte la hora en un objeto datetime
            time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H%M%S.%f")

            # print('Imagen recibida y guardada correctamente.')
            # print(f'Hora de la toma de la imagen: {time_obj}')

            # Cierra la conexión
        except Exception as e:
            # Código que se ejecuta en caso de una excepción
            print('Ocurrió una excepción: probalbemente nad ane el buffer')
    conn.close()

def start_server():
    pool = mp.Pool(4)
    # Crea un socket y espera a que un cliente se conecte
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP_ADDRESS, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        pool.apply_async(process_image, args=(conn, addr))

        # Cerrar pool de procesos
        #img = cv2.imread('E:\\resposGit\\codigo-memoria\\TestSockets\\imagenes_capturadas\\7-2023-04-10 114933.078472.jpg')
        #cv2.imshow('Imagen', img)
        # Esperamos 5 segundos antes de detener los procesos
        # esperamos 20 milisegundos a que se presione una tecla
        key = cv2.waitKey(20)
        if key == ord('q'):  # salimos si se presiona la tecla 'q'
            break
    pool.close()
    pool.join()


if __name__ == "__main__":
    start_server()

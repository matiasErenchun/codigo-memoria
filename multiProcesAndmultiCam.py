import time
from multiprocessing import Process, Queue
import os
import cv2
import pickle
import struct
import socket


def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_FPS, 15)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


class Mensaje:
    def __init__(self, tipo, name, frame):
        self.tipo = tipo
        self.name = name
        self.frame = frame


def info(cola, nombre, camid):
    cam = cv2.VideoCapture(camid)
    cam.set(cv2.CAP_PROP_FPS, 15)
    continuar = True
    i = 0
    while (continuar and i < 10):

        if cam.isOpened():  # try to get the first frame
            rval, frame = cam.read()
        else:
            rval = False
            continuar = False
        while rval and i < 10:
            messajes = Mensaje('on', nombre, frame)
            cola.put(messajes)
            rval, frame = cam.read()
            i += 1
    if continuar:
        men = Mensaje('off', nombre, os.getpid())
        cola.put(men)

def send(client_socket, frame):
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.38'
    port = 9999
    client_socket.connect((host_ip, port))

    cv2.namedWindow("prin")
    mcola = Queue()
    print('pid main:', os.getpid())
    p = Process(target=info, args=(mcola, 'juan', 0,))
    t = Process(target=info, args=(mcola, 'pepe', 1,))
    p.start()
    t.start()
    continuarP = True
    continuarT = True
    count = 1
    while continuarP or continuarT:
        if mcola.qsize() > 0:
            messaje = mcola.get()
            if messaje.tipo != 'on':
                if messaje.name == 'juan':
                    continuarP = False
                else:
                    continuarT = False
            else:
                #cv2.imwrite('D:\\basura\\img-%05d.jpg' % count, messaje.frame)
                send(client_socket, messaje.frame)
                print(messaje.tipo + " ," + messaje.name)
                count += 1
    p.join()
    t.join()
    client_socket.close()

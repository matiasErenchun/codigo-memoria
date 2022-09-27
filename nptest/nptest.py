import time
import cv2
import numpy as np
from multiprocessing import Process, Queue
import random
import os
from vidgear.gears import NetGear

class Mensaje:
    def __init__(self, tipo, name, frame):
        self.tipo = tipo
        self.name = name
        self.frame = frame


def info(cola, nombre, pathimg):
    img = cv2.imread(pathimg)
    image_np = np.array(img)
    while (True):
        men = Mensaje('on', nombre, image_np)
        cola.put(men)
        time.sleep(random.uniform(0.3,1))


if __name__ == '__main__':
    mcola = Queue()
    IMAGE_PATH1 = "D:\\fotos pajaros\\train\\train\\357 Sharp-shinned Hawk (Adult )57.jpg"
    IMAGE_PATH2 = "D:\\fotos pajaros\\train\\test\\298 Swainson's Hawk (Dark morph )0.jpg"
    print('pid main:', os.getpid())
    p = Process(target=info, args=(mcola, 'juan', IMAGE_PATH1,))
    t = Process(target=info, args=(mcola, 'pepe', IMAGE_PATH2,))
    p.start()
    t.start()
    while True:
        if mcola.qsize() > 0:
            messaje = mcola.get()
            image_np = messaje.frame
            cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    p.terminate()
    t.terminate()
    print("Bye, Bye Bro")

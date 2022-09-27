

import os
import numpy as np


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

from multiprocessing import Queue, Process
import cv2
if __name__ == '__main__':
    mcola = Queue()
    p = Process(target=info, args=(mcola, 0,))
    t = Process(target=info, args=(mcola, 1,))
    p.start()
    t.start()
    while True:
        if mcola.qsize() > 0:
            image_np = mcola.get()
            cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    p.terminate()
    t.terminate()
    print("Bye, Bye Bro")
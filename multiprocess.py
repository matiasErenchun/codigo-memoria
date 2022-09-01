import time
from multiprocessing import Process, Queue
import os
import random


class Mensaje:
    def __init__(self, tipo, name, pid):
        self.tipo = tipo
        self.name = name
        self.pid = pid


def info(cola, nombre):
    i = 0
    continuar = True
    while (i < 10 and continuar):
        a = random.randint(1,10)
        if a > 8:
            men = Mensaje('off', nombre, os.getpid())
            continuar = False
        else:
            men = Mensaje('on', nombre, os.getpid())
        cola.put(men)
        i += 1
        time.sleep(0.5)
    if continuar:
        men = Mensaje('off', nombre, os.getpid())
        cola.put(men)


if __name__ == '__main__':
    mcola = Queue()
    print('pid main:', os.getpid())
    p = Process(target=info, args=(mcola, 'juan',))
    t = Process(target=info, args=(mcola, 'pepe',))
    p.start()
    t.start()
    continuarP = True
    continuarT = True
    while continuarP or continuarT:
        if mcola.qsize() > 0:
            messaje = mcola.get()
            if messaje.tipo != 'on':
                if messaje.name == 'juan':
                    continuarP = False
                else:
                    continuarT = False
            print(messaje.tipo + " ," + messaje.name + " ," + str(messaje.pid))

    p.join()
    t.join()

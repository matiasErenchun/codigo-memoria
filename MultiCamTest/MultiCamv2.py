import multiprocessing
import random
import cv2


def child_process(stop_event, i):
    while not stop_event.is_set():
        print(str(i) + ": " + str(random.randint(1, 100)))


if __name__ == '__main__':
    # Creamos un evento para indicar a los procesos que deben detenerse
    stop_event = multiprocessing.Event()

    # Creamos dos procesos hijos
    processs= []
    for i in range(2):
        p = multiprocessing.Process(target=child_process, args=(stop_event, i,))
        p.start()
        processs.append(p)

    # Iniciamos los procesos

    img = cv2.imread('E:\\resposGit\\codigo-memoria\\TestSockets\\imagenes_capturadas\\71-2023-04-10 115549.362633.jpg')
    cv2.imshow('Imagen', img)
    # Esperamos 5 segundos antes de detener los procesos
    while True:
        # esperamos 20 milisegundos a que se presione una tecla
        key = cv2.waitKey(20)
        if key == ord('q'):  # salimos si se presiona la tecla 'q'
            stop_event.set()
            break
    cv2.destroyAllWindows()
    for p in processs:
        p.join()

    # Indicamos a los procesos que deben detenerse

    # Esperamos a que los procesos hijos finalicen su ejecución

    print('Los procesos han terminado.')

import socket
from time import sleep

i = 0
while (i < 10):
    mi_socket = socket.socket()
    mi_socket.connect(('192.168.1.38', 8888))
    mensaje = str(i) + " mensaje"
    mi_socket.send(str.encode(mensaje))
    mi_socket.close()
    sleep(1)
    i += 1
print("bye bye bro")

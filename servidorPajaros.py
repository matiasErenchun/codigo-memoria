import socket

mi_socket = socket.socket()
mi_socket.bind(('192.168.1.38',8888))
mi_socket.listen(2)
while True:
    conexion, addr = mi_socket.accept()
    print('conexion entrante desde:'+ str(addr))
    informacionEntrante = conexion.recv(1024)
    print(str(informacionEntrante))


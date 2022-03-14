import socket, cv2, pickle, struct
from time import sleep

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.38'
port = 9999
client_socket.connect((host_ip, port))

while True:
    vid = cv2.VideoCapture(0)
    while vid.isOpened():
        img, frame = vid.read()
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    break
cv2.destroyWindow('TRANSMITTING VIDEO')
client_socket.close()


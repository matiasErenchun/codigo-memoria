import socket, cv2, pickle, struct

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
host_ip = '192.168.1.38'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)
data = b""
payload_size = struct.calcsize("Q")
# Socket Accept
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)
continuar = True
while continuar:
    if client_socket:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet:
                continuar = False
                break
            data += packet
        if continuar:
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
cv2.destroyWindow("RECEIVING VIDEO")
client_socket.close()

import socket

connection = socket.socket (socket.AF_INET,socket.SOCK_STREAM)
connection.connect(("192.168.240.95",4444))

message = "Successfully Connected."
connection.sendto(message.encode(),("192.168.240.95",4444))

receive_data = connection.recv(1024)
print(receive_data)

connection.close()
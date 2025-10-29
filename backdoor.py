import socket,os, time, threading, sys
from queue import Queue

intThreads = 2
arrJobs = [1,2]
queue = Queue()

arrAddresses = []
arrConnections = []

strHost = "192.168.1.11"
intPort = 4444

intBuff = 1024

decode_utf = lambda data: data.decode("utf-8")

remove_quotes = lambda string: string.replace("\"","")

send = lambda data: conn.send(data)

recv = lambda buffer: conn.recv(buffer)

def recvall(buffer):
    bytData = b""
    while True:
        bytPart = recv(buffer)
        if len (bytPart) == buffer:
            return bytPart
        bytData += bytPart

        if len(bytData) == buffer:
            return bytData
        
def create_socket():
    global objSocket
    try:
        objSocket = socket.socket()
        objSocket.setsockopt(socket.SQL_SOCKET,socket.SO_REUSEADDR,1)

    except socket.error() as strError:
        print("Error creating socket"+str(strError))

def socket_bind():
    global objSocket
    try:
        print("Listening on port:"+ str(intPort))
        objSocket.bind((strHost,intPort))
        objSocket.Listen(20)

    except socket.error() as strError:
        print("Error binding socket "+str(strError))
        socket_bind()

def socket_accept():
    while True:
        try:
            conn, address = objSocket.accept()
            conn.setblocking(1) #no timeout
            arrConnections.append(conn)
            client_info = decode_utf(conn.recv(intBuff)).split("',")

            address += client_info[0], client_info[1], client_info[2]
            arrAddresses.append(address)
            print("\n"+"Connection has been established : {0} ({1})".format(address[0],address[2]))

        except socket.error:
            print("Error accepting connections!")
            continue


    
    #multithreading

def create_threads():
    for _ in range(intThreads):
        objThread = threading.Thread()

def work():
    while True:
        intValue = queue.get()
        if intValue == 1:
            create_socket()
            socket_bind()
            socket_accept()

        elif intValue == 2:
            while True:
                time.sleep(0.2)
                if len(arrAddresses) > 0:
                    #main_menu()
                    break


        queue.task_done()
        queue.task_done()
        sys.exit(0)





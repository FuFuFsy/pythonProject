from socket import *

# Define the client name
HOST = '192.168.137.1'
PORT = 21599
BUFSIZE = 1024
ADDR = (HOST, PORT)

# connect to the server
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
    data = input('(please input the information of share, format like 20201112,HSI),date range(20201112--20210305),sharename（share000547,HSI）\n')
    if not data:
        break
    # input the message,the send function receives the message as byte which needs to be encoded
    tcpCliSock.send(bytes(data, 'utf-8'))
    data_rec = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    print(data_rec.decode('utf-8'))
tcpCliSock.close()
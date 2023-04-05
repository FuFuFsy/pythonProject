from socket import *
from time import ctime
import data_storing, costants, data_acquisition
# Define the server
HOST = ''
PORT = 21599
BUFSIZE = 1024
ADDR = (HOST, PORT)

# Define the server properties
tcpsersock = socket(AF_INET, SOCK_STREAM)
tcpsersock.bind(ADDR)
tcpsersock.listen(5)

while True:
    print('Waiting for connection...')
    tcpcliscock, addr = tcpsersock.accept()
    print('...Connect：', addr)

    while True:
        data = tcpcliscock.recv(BUFSIZE)
        if not data:
            break
        # Receive message
        data_rcv=data.decode('utf-8')
        # date_send = '[%s]%s' % (ctime(), data.decode('utf-8'))
        data_split=data_rcv.split(",")
        print(data_split)
        date=data_split[0]
        share=data_split[1]
        if share=='HSI':
            data =data_acquisition.get_from_Share_HSI(conditionproduct={"date": date})
        if share=='share000547':
            data = data_acquisition.acquire_from_database(conditionproduct={"date": date})
        # data = data_acquisition.get_from_products(conditionproduct={"date": data_rcv})
        print(data)
        data=data[0]
        print(data['predict_close'])
        data=str(data['predict_close'])
        data="the prediction of "+share+" closing price is:"+data
        tcpcliscock.send(data.encode('utf-8'))
    tcpcliscock.close()

tcpsersock.close()
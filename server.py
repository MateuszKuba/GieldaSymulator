import socket
import pickle

PORT = 5000

class ClientServer():
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        #try:
            self.clientsocket.connect(('localhost', PORT))
            return True
       # except OSError as e:
        #    print(e)
            
    def send(self,msg):
        try:
            data = pickle.dumps(msg)
            self.clientsocket.send(data)
        finally:
            self.clientsocket.close()
    
class StockMarketServer():
    def __init__(self):
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind(('localhost', PORT))
        # become a server socket
        self.serversocket.listen(5)
        
    def listen_for_data(self):
        while True:
            # accept connections from outside
            (clientsocket, address) = self.serversocket.accept()
            
            try:
                print('Connected by', address)
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                buf = clientsocket.recv(4092)
                buf = pickle.loads(buf)
                print(buf)
                if len(buf) > 0:
                    return buf
            except KeyboardInterrupt:
                if clientsocket:
                    clientsocket.close()
            finally:
                clientsocket.close()

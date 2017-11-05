from gevent import socket
from gevent.server import StreamServer
import pickle


PORT = 5001

class ClientServer():
    import socket
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
        self.buf=None
        server = StreamServer(
                    ('localhost', PORT), self.handle_echo)
        print(server)
        server.serve_forever()
    
    def handle_echo(self,sock, address):
        buf = sock.recv(4092)
        if buf:
            buf = pickle.loads(buf)
            sock.shutdown(socket.SHUT_WR)
            sock.close()
            self.buf = buf
            print(self.buf)
    
    def listen_for_data(self):
        while True:
            if self.buf!=None:
                return self.buf
        
            
        

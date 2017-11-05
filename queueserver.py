class ClientServer():
    def __init__(self,order_list):
        self.order_list = order_list
            
    def send(self,msg):
        self.order_list.put(msg)

    
class StockMarketServer():
    def __init__(self,order_list):
        self.order_list = order_list
    
    def listen_for_data(self):
            if not self.order_list.empty():
                data = self.order_list.get()
                return data


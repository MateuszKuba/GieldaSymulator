from queueserver import StockMarketServer
import json
import datetime
#from threading import Lock


class StockMarket(StockMarketServer):

    def __init__(self,order_list):
        self.ask = None
        self.bid = None
        self.last_ask_price = 101
        self.last_bid_price = 100
        self.transaction_ask = []
        self.transaction_bid = []
        self.transaction_list = []
        StockMarketServer.__init__(self,order_list)
       # self._time = str(datetime.datetime.now()).split('.')
        
    def add_transaction(self,direction,user_id):
        '''
        It will check if there is a market price for opposite position , otherwise
        it will put limit price
        '''
        if direction == 1:
            self.transaction_market_if_possible(direction,user_id)
            self.transaction_limit_if_possible(direction,user_id)
        
        if direction == -1:
            self.transaction_market_if_possible(direction,user_id)
            self.transaction_limit_if_possible(direction,user_id)

    def transaction_market_if_possible(self,direction,user_id):
        if direction == 1:
            if self.ask is not None:
                t = self.transaction_ask.pop()
                self.transaction_clearing(direction,t,liquidity_taker_user_id = user_id)
        if direction == -1:
            if self.bid is not None:
                t = self.transaction_bid.pop()
                self.transaction_clearing(direction,t,liquidity_taker_user_id = user_id)

    def transaction_limit_if_possible(self,direction,user_id):
        if direction == -1:
            if self.bid is None:
                trans = None
                if self.ask is not None:
                    trans = Transaction(self.ask - 1, user_id, "sell_limit")
                    self.ask = self.ask - 1
                else:
                    trans = Transaction(self.last_ask_price, user_id, "sell_limit")
                    self.ask = self.last_ask_price
                self.transaction_ask.append(trans)
                self.transaction_list.append(trans)
        if direction == 1:
            if self.ask is None:
                trans = None
                if self.bid is not None:
                    trans = Transaction(self.bid + 1,user_id,"buy_limit")
                    self.bid = self.bid+1
                else:
                    trans = Transaction(self.last_bid_price,user_id,"buy_limit")
                    self.bid = self.last_bid_price
                self.transaction_bid.append(trans)
                self.transaction_list.append(trans)

    def remove_transaction(self,user_id):
        print("remove")
        
    def listen_for_orders(self, th_stop):
        while not th_stop.is_set():
            buf = self.listen_for_data()
            if buf is not None:
                #lock = Lock()
                #with lock:
                    order,user_id = buf
                    if order == 1:
                        self.add_transaction(1, user_id)
                    else:
                        self.add_transaction(-1, user_id)
                    buf = None
    
                
    def transaction_clearing(self,direction,transaction,liquidity_taker_user_id):
        '''
        Write short and long positions to database depending on trade direction
        '''
        if direction == 1:
            self.clearing_long_positions(transaction, liquidity_taker_user_id)
        if direction == -1:
            self.clearing_short_positions(transaction, liquidity_taker_user_id)

    def clearing_long_positions(self,transaction,liquidity_taker_user_id):

        price = transaction.parameters.get('sell_limit')[0]
        user_id = transaction.parameters.get('sell_limit')[1]

        self.update_ask_price()

        t = Transaction(price, (user_id, liquidity_taker_user_id), "buy")
        self.transaction_list.append(t)
        self.write_json(t.parameters)

    def update_ask_price(self):
        '''
        Check if there is a price waiting in array with ask prices,
        if yes update, if no set ask to None
        '''
        if self.transaction_ask:
            self.ask = self.transaction_ask[-1].parameters.get("sell_limit")[0]
        else:
            self.ask = None

    def clearing_short_positions(self,transaction,liquidity_taker_user_id):
        '''sell market czyli matchuje z buy limit

                Jeżeli transakcja jest spadmowa to wez parametry tej transakcji szukajac po buy limit,
                nastepnie jezeli drabinka transakcji bid ( buy limit ) nie jest pusta to wez ostatnia cene z niej,
                jezeli jest pusta to ustaw cene bid po tej transakcji na 0, nastepnie utworz obiekt transakcji
                 dodaj do listy transakcji te transakcje oraz do pliku, dla transakcji zapisuje dawce plynnosci
                 czyli user_id z transakcji buy_limit oraz user_id dla tej transakcji przekazane jako liquidity_taker_id

        '''

        # price and user_id of the closest buy_limit price in ladder
        price = transaction.parameters.get('buy_limit')[0]
        user_id = transaction.parameters.get('buy_limit')[1]

        self.update_bid_price()

        self.last_bid_price = price
        t = Transaction(price, (user_id, liquidity_taker_user_id), "sell")
        self.transaction_list.append(t)
        self.write_json(t.parameters)

    def update_bid_price(self):
        '''
        Check if there is a price waiting in array with bid prices,
        if yes update, if no set bid to None
        '''

        if self.transaction_bid:
            self.bid = self.transaction_bid[-1].parameters.get("buy_limit")[0]
        else:
            self.bid = None
            
    def write_json(self,data):
        #i = self._time
        i = "_1"
        with open('data_{}.txt'.format(i), 'a') as outfile:
            json.dump(data, outfile,) #indent
            outfile.write('\n')


class Transaction():
    def __init__(self,price,user,transaction_type):
        #self.price = price
        #self.user = user
        #self.transaction_type = transaction_type
        self.parameters = {transaction_type : ( price, user )}
        
        
class Price():
    def __init__(self,price,user_id):
        self.price = price
        self.user_id = user_id
    def set_price(self,price,user_id):
        self.price = price
        self.user_id = user_id
        
        
class AskPrice(Price):
    def __init__(self,price,user_id):
        super().__init__(self,price,user_id)


class BidPrice(Price):
    def __init__(self,price,user_id):
        super().__init__(self,price,user_id)
        
      

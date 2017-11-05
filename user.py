from preferences import Preferences
from numpy import random as rand
from queueserver import ClientServer


class User:
    
    def __init__(self,user_id,order_list,leverage = 3):
        self.preferences = Preferences()
        self.account_balance = 100
        self.account_sentiment = 0
        self.user_id = user_id
        self.connection = ClientServer(order_list)
        self.execution_delay = True
        self.max_sentiment = leverage

    def set_random_slippage(self, slippage = True):
        self.execution_delay = slippage

    def make_transaction(self,direction):
        import random, time
        ### random slippage ###
        if self.execution_delay:
            time.sleep(random.uniform(0.01,0.5))
        if direction == 1 and self.account_sentiment != self.max_sentiment:
                self.account_sentiment += 1
                self.connection.send([1,self.user_id ])

        if direction == -1 and self.account_sentiment != -self.max_sentiment:
                self.account_sentiment -= 1
                self.connection.send([-1,self.user_id ])

    def random_direction(self, ratio):
        '''
        Do random choice between buying ( 1 ) or selling ( -1 ) using
        ratio between 0. and 1.0
        '''
        return rand.choice([1,-1],p=[1-ratio,ratio])

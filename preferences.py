class Preferences:
    
    def __init__(self):
        self.rising = 3
        self.lowering = 1
        
    def set_preferencje(self,rising,lowering):
        self.rising = rising
        self.lowering = lowering
        
    def get_ratio(self):
        return self.rising/self.lowering
        
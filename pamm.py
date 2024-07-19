import math

class PredictionMarket:
    def __init__(self, b=100):
        self.b = b  # Liquidity parameter
        self.shares = {'yes': 0, 'no': 0}  # shares outstanding 
        # self.outcome = None  # None means the outcome is not decided yet
        self.pool = 0 # money in the pool 

    def price(self):
        # Calculate current prices using LMSR
        total_shares = self.shares['yes'] + self.shares['no']
        p_yes = math.exp(self.shares['yes'] / self.b) / (math.exp(self.shares['yes'] / self.b) + math.exp(self.shares['no'] / self.b))
        p_no = math.exp(self.shares['no'] / self.b) / (math.exp(self.shares['yes'] / self.b) + math.exp(self.shares['no'] / self.b))
        return {'yes': p_yes, 'no': p_no}

    def buy_shares(self, side, amount):
        total_price = 0 
        for i in range(amount): 
            total_price += self.price()[side]
            self.shares[side] += 1 
        self.shares[outcome] += amount
        return total_price
    
    def sell_shares(self, side, amount):
        total_gain = 0 
        for j in range(amount):
            total_gain += self.price()[side]
            self.shares[side] += 1 
        self.shares[outcome] -= amount
        return total_gain  
    
    def get_price(self): 
        print(self.price()) 

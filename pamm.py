import math

class PredictionMarket:
    def __init__(self, b=1):
        self.b = b  # Liquidity parameter
        self.shares = {'yes': 0, 'no': 0}  # Shares outstanding
        self.pool = 0  # Money in the pool

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
        self.pool += total_price
        return total_price
    
    def sell_shares(self, side, amount):
        total_gain = 0 
        for j in range(amount):
            total_gain += self.price()[side]
            self.shares[side] -= 1 
        self.pool -= total_gain
        return total_gain
    
    def get_price(self): 
        return self.price()

class Player:
    def __init__(self, name):
        self.name = name
        self.balance = {'yes': 0, 'no': 0}
        self.money = 100

def player_turn(player, market):
    print(f"\n{player.name}'s turn:")
    print(f"Balances - Yes: {player.balance['yes']}, No: {player.balance['no']}, Money: {player.money}")

    prices = market.get_price()
    print(f"Current prices: Yes: {prices['yes']:.4f}, No: {prices['no']:.4f}")

    action = input("Do you want to buy or sell? ").strip().lower()
    side = input("Which side (yes or no)? ").strip().lower()

    while True:
        amount = int(input("For what amount? ").strip())
        if action == 'buy':
            total_price = sum(market.price()[side] for _ in range(amount))
            if total_price <= player.money:
                player.money -= total_price
                market.buy_shares(side, amount)
                player.balance[side] += amount
                print(f"{player.name} bought {amount} shares of {side} for a total price of {total_price:.2f}.")
                break
            else:
                print(f"Not enough money. You need {total_price:.2f} but have {player.money:.2f}. Please enter a smaller amount.")
        elif action == 'sell':
            if player.balance[side] >= amount:
                total_gain = market.sell_shares(side, amount)
                player.money += total_gain
                player.balance[side] -= amount
                print(f"{player.name} sold {amount} shares of {side} for a total gain of {total_gain:.2f}.")
                break
            else:
                print(f"Not enough shares to sell. You have {player.balance[side]} shares of {side}. Please enter a smaller amount.")
        else:
            print("Invalid action. Please enter 'buy' or 'sell'.")

    prices = market.get_price()
    print(f"Updated prices: Yes: {prices['yes']:.4f}, No: {prices['no']:.4f}")
    print(f"Updated balances - Yes: {player.balance['yes']}, No: {player.balance['no']}, Money: {player.money}")

def main():
    market = PredictionMarket()
    players = [Player('Player 1'), Player('Player 2'), Player('Player 3')]

    while True:
        for player in players:
            player_turn(player, market)
        
        continue_game = input("Do you want to continue the game? (yes/no) ").strip().lower()
        if continue_game != 'yes':
            break

if __name__ == "__main__":
    main()

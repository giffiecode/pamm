import math

class PredictionMarket:
    def __init__(self, b=10):
        self.b = b  # Liquidity parameter
        self.shares = {'yes': 100, 'no': 200}  # Initial shares
        self.pool = 0  # Initial pool of money
        self.fee_percentage = 0.02  # Transaction fee percentage

    def price(self):
        total_shares = self.shares['yes'] + self.shares['no']
        p_yes = math.exp(self.shares['yes'] / self.b) / (math.exp(self.shares['yes'] / self.b) + math.exp(self.shares['no'] / self.b))
        p_no = math.exp(self.shares['no'] / self.b) / (math.exp(self.shares['yes'] / self.b) + math.exp(self.shares['no'] / self.b))
        return {'yes': p_yes, 'no': p_no}

    def buy_shares(self, side, amount):
        total_price = 0
        for i in range(amount):
            total_price += self.price()[side]
            self.shares[side] += 1
        fee = total_price * self.fee_percentage
        self.pool += total_price + fee
        return total_price + fee

    def sell_shares(self, side, amount):
        total_gain = 0
        for j in range(amount):
            total_gain += self.price()[side]
            self.shares[side] -= 1
        fee = total_gain * self.fee_percentage
        self.pool -= (total_gain - fee)
        return total_gain - fee

    def get_price(self):
        return self.price()

    def get_pool(self):
        return self.pool

class Player:
    def __init__(self, name):
        self.name = name
        self.balance = {'yes': 0, 'no': 0}
        self.money = 100

def player_turn(player, market):
    print(f"\n{player.name}'s turn:")
    print(f"Balances - Yes: {player.balance['yes']}, No: {player.balance['no']}, Money: {player.money}")
    print(f"Current pool money: {market.get_pool():.2f}")

    prices = market.get_price()
    print(f"Current prices: Yes: {prices['yes']:.4f}, No: {prices['no']:.4f}")

    action = input("Do you want to buy or sell? ").strip().lower()
    side = input("Which side (yes or no)? ").strip().lower()

    while True:
        amount = int(input("For what amount? ").strip())
        if action == 'buy':
            total_price = sum(market.price()[side] for _ in range(amount))
            total_price_with_fee = total_price * (1 + market.fee_percentage)
            if total_price_with_fee <= player.money:
                player.money -= total_price_with_fee
                market.buy_shares(side, amount)
                player.balance[side] += amount
                print(f"{player.name} bought {amount} shares of {side} for a total price of {total_price_with_fee:.2f} (including fee).")
                break
            else:
                print(f"Not enough money. You need {total_price_with_fee:.2f} but have {player.money:.2f}. Please enter a smaller amount.")
        elif action == 'sell':
            if player.balance[side] >= amount:
                total_gain = sum(market.price()[side] for _ in range(amount))
                total_gain_with_fee = total_gain * (1 - market.fee_percentage)
                if total_gain_with_fee <= market.pool:
                    player.money += total_gain_with_fee
                    market.sell_shares(side, amount)
                    player.balance[side] -= amount
                    print(f"{player.name} sold {amount} shares of {side} for a total gain of {total_gain_with_fee:.2f} (after fee).")
                    break
                else:
                    print(f"The market pool does not have enough funds to pay you. Please enter a smaller amount.")
            else:
                print(f"Not enough shares to sell. You have {player.balance[side]} shares of {side}. Please enter a smaller amount.")
        else:
            print("Invalid action. Please enter 'buy' or 'sell'.")

    prices = market.get_price()
    print(f"Updated prices: Yes: {prices['yes']:.4f}, No: {prices['no']:.4f}")
    print(f"Updated balances - Yes: {player.balance['yes']}, No: {player.balance['no']}, Money: {player.money}")
    print(f"Remaining pool money: {market.get_pool():.2f}")

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

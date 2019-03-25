from cs50 import SQL
from time import sleep
from helpers import lookup

db = SQL("sqlite:///finance.db")

session = {'user_id': 3}

# history = db.execute("SELECT * FROM history WHERE user_id = :i", i = session['user_id'])
# print("Records from history", history)
# users = db.execute("SELECT * FROM users WHERE id = :i", i = session['user_id'])
# print("Records from users", users)
# accounts = db.execute("SELECT * FROM accounts WHERE user_id = :i", i = session['user_id'])
# print("Records from accounts", accounts)


user_cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session['user_id'])
accounts = db.execute("SELECT * FROM accounts WHERE user_id = :i", i=session['user_id'])
total_cash = user_cash[0]['cash']
print(user_cash)

# Calculate current value of shares
for row in accounts:
    # Each row contains information about shares of one company
    ticker = row['symbol']
    amount = row['amount']
    # Knowing amount and ticker get current price and get present value of shares
    pricing = lookup(ticker)
    row['price'] = pricing['price'] * amount
    print(row['price'])
    total_cash += row['price']
    row['current_price'] = pricing['price']
    print(total_cash)
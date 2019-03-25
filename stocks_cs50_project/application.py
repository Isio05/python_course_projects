import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from time import sleep

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session['user_id'])
    accounts = db.execute("SELECT * FROM accounts WHERE user_id = :i", i=session['user_id'])
    total_cash = user_cash[0]['cash']
    total_shares = 0

    # Calculate current value of shares
    for row in accounts:
        # Each row contains information about shares of one company
        ticker = row['symbol']
        amount = row['amount']
        # Knowing amount and ticker get current price and get present value of shares
        pricing = lookup(ticker)
        row['price'] = pricing['price'] * amount
        total_cash += row['price']
        total_shares += row['price']
        row['current_price'] = pricing['price']

    return render_template("index.html", cash=user_cash[0]['cash'], total=total_cash, accounts=accounts, total_shares=total_shares)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        ticker = request.form.get("symbol")
        ticker = ticker.lower()
        amount = request.form.get("shares")

        # Check amount to be positive integer
        if amount == "":
            return apology("Amount field must be positive integer", 400)
        for i in amount:
            if i not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9) and i not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                return apology("Amount field must be positive integer", 400)
        amount = int(amount)

        pricing = lookup(ticker)

        if not pricing:
            return apology("Invalid ticker", 400)
        else:
            current_price = pricing['price']

        # Check if the user have enough cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session['user_id'])
        if user_cash[0]['cash'] < (amount * current_price):
            return apology("Not enough money", 400)
        # Check if user already has shares of the company
        elif (db.execute("SELECT * FROM accounts WHERE user_id = :i AND symbol = :s", i=session['user_id'], s=ticker)):
            # Add shares to the existing record
            existing = db.execute("SELECT * FROM accounts WHERE user_id = :i AND symbol = :s", i=session['user_id'], s=ticker)
            db.execute("UPDATE accounts SET amount = :a WHERE user_id = :i AND symbol = :s",
                       a=existing[0]['amount'] + amount, i=session['user_id'], s=ticker)
            # Subtract cash from account
            db.execute("UPDATE users SET cash = :c WHERE id = :i",
                       c=user_cash[0]['cash'] - amount * current_price, i=session['user_id'])
            db.execute("INSERT INTO history (user_id, symbol, price, amount, type) VALUES (:u, :s, :p, :a, :t)",
                       u=session['user_id'], s=ticker, p=current_price, a=amount, t='buy')
        # If users does not have any of company shares, execute:
        else:
            # Add shares to the user account
            db.execute("INSERT INTO accounts (user_id, symbol, price, amount) VALUES (:u, :s, :p, :a)",
                       u=session['user_id'], s=ticker, p=current_price, a=amount)
            # Subtract cash from account
            db.execute("UPDATE users SET cash = :c WHERE id = :i",
                       c=user_cash[0]['cash'] - amount * current_price, i=session['user_id'])
            db.execute("INSERT INTO history (user_id, symbol, price, amount, type) VALUES (:u, :s, :p, :a, :t)",
                       u=session['user_id'], s=ticker, p=current_price, a=amount, t='buy')

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        ticker = request.form.get("symbol")
        ticker = ticker.lower()
        amount = request.form.get("shares")

        # Check amount to be positive integer
        if amount == "":
            return apology("Amount field must be positive integer", 400)
        for i in amount:
            if i not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9) and i not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                return apology("Amount field must be positive integer", 400)
        amount = int(amount)

        pricing = lookup(ticker)

        if not pricing:
            return apology("Invalid ticker", 400)
        else:
            current_price = pricing['price']

        user_cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session['user_id'])
        user_amount = db.execute("SELECT amount FROM accounts WHERE user_id = :i AND symbol = :s",
                                 i=session['user_id'], s=ticker)
        # Check if user have enough amount of shares to sell
        if not user_amount:
            return apology("No shares with such ticker", 400)
        elif user_amount[0]['amount'] < amount:
            return apology("Not enough shares to sell", 400)

        # Remove shares from the user account
        db.execute("UPDATE accounts SET amount = :a WHERE user_id = :i AND symbol = :s",
                   a=user_amount[0]['amount'] - amount, i=session['user_id'], s=ticker)
        # Add cash to account
        db.execute("UPDATE users SET cash = :c WHERE id = :i",
                   c=user_cash[0]['cash'] + amount * current_price, i=session['user_id'])
        db.execute("INSERT INTO history (user_id, symbol, price, amount, type) VALUES (:u, :s, :p, :a, :t)",
                   u=session['user_id'], s=ticker, p=current_price, a=amount, t='sell')

        return redirect("/")

    else:
        return render_template("sell.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    h = db.execute("SELECT * FROM history WHERE user_id = :i", i=session['user_id'])

    return render_template("history.html", history=h)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == 'POST':
        pricing = lookup(request.form.get("symbol"))

        if not pricing:
            return apology("Invalid ticker", 400)

        return render_template("quoted.html", data=pricing)

    else:
        return render_template("quote.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was corectly retyped
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        elif db.execute("SELECT * FROM users WHERE username = :n", n=request.form.get("username")):
            return apology("User already exists")

        # Otherwise add user to database and return to homepage
        else:
            result = db.execute("INSERT INTO users (username, hash) VALUES (:username,:hash)",
                                username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

            if not result:
                return apology("User already exists", 400)

            db_id = db.execute("SELECT id FROM users WHERE username = :username", username=request.form.get("username"))

            session['user_id'] = db_id[0]['id']

            return redirect("/")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

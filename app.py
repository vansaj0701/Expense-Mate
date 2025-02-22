from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    total_income_query = cur.execute("SELECT amount FROM users WHERE user_id=?", (user_id,))
    total_income = list(total_income_query)[0][0]

    expenses_query = cur.execute("""
                           SELECT category, SUM(amount)
                           FROM expenses
                           WHERE user_id = ?
                           GROUP BY category
                           ORDER BY category
                           """, (user_id,)
                           )
    expenses = dict(expenses_query)

    total_expense_query = cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?", (user_id,))
    total_expense = list(total_expense_query)[0][0]

    current_balance = total_income - total_expense

    history = cur.execute("""
                          SELECT category, amount, date_added
                          FROM expenses
                          WHERE user_id=?
                          ORDER BY date_added DESC
                          LIMIT 8
                          """, (user_id,)
                          )

    return render_template("index.html", total_income=total_income,
                           expenses=expenses, total_expense=total_expense,
                           current_balance=current_balance, history=history,
                           )


@app.route("/register", methods=["GET", "POST"])
def register():
    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        amount = request.form.get("total-income")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")
        if not name:
            return render_template("error.html", message="Name not provided")

        if not email:
            return render_template("error.html", message="Email address not provided")

        if not amount:
            return render_template("error.html", message="Total income not provided")

        if not password:
            return render_template("error.html", message="Password not provided")

        if not confirm_password:
            return render_template("error.html", message="Confirm password not provided")

        if password != confirm_password:
            return render_template("error.html", message="Password doesn't match")

        hash = generate_password_hash(password)

        try:
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cur.fetchone():
                return render_template("error.html", message="Email is already registered")

            new_user = cur.execute("INSERT INTO users (name, email, amount, password) VALUES (?, ?, ?, ?)",
                                   (name, email, amount, hash))
            conn.commit()

            # session["user_id"] = new_user

            return redirect("/login")

        except:
            return render_template("error.html", message="Try again later")

        finally:
            conn.close()

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()

    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return render_template("error.html", message="Email address not provided")

        if not password:
            return render_template("error.html", message="Password not provided")

        row = cur.execute(
            "SELECT user_id, password FROM users WHERE email = ?", (email,)
        ).fetchone()

        if row is None:
            return render_template("error.html", message="Invalid username and/or password")

        hashed_password = row[1]

        if not check_password_hash(hashed_password, password):
            return render_template("error.html", massage="invalid username and/or password")

        session["user_id"] = row[0]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/new", methods=["GET", "POST"])
def new():
    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("type")
        date = request.form.get("date")

        if not amount:
            return render_template("error.html", message="Email address not provided")

        if not category:
            return render_template("error.html", message="Password not provided")

        if not date:
            return render_template("error.html", message="Date not provided")

        cur.execute("INSERT INTO expenses(user_id, category, date_added) VALUES (?, ?, ?)", (user_id, category, date))
        conn.commit()

        return redirect("/")

    else:
        return render_template("new.html")

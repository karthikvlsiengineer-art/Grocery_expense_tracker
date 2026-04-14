from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        amount REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_db()

    if request.method == "POST":
        item = request.form["item"]
        amount = request.form["amount"]
        date = request.form["date"]

        conn.execute(
            "INSERT INTO expenses(item,amount,date) VALUES (?,?,?)",
            (item, amount, date)
        )

        conn.commit()
        return redirect("/")

    expenses = conn.execute("SELECT * FROM expenses").fetchall()

    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]

    if total is None:
        total = 0

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/chart-data")
def chart_data():

    conn = get_db()

    # Pie Chart (Item vs Expense)
    items = conn.execute("""
        SELECT item, SUM(amount) as total
        FROM expenses
        GROUP BY item
    """).fetchall()

    item_labels = [row["item"] for row in items]
    item_values = [row["total"] for row in items]

    # Bar Chart (Monthly Expense)
    months = conn.execute("""
        SELECT strftime('%Y-%m', date) as month,
        SUM(amount) as total
        FROM expenses
        GROUP BY month
    """).fetchall()

    month_labels = [row["month"] for row in months]
    month_values = [row["total"] for row in months]

    conn.close()

    return jsonify({
        "item_labels": item_labels,
        "item_values": item_values,
        "month_labels": month_labels,
        "month_values": month_values
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
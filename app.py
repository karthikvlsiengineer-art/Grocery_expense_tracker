from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


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


# GET ALL EXPENSES
@app.route("/expenses", methods=["GET"])
def get_expenses():

    conn = get_db()

    expenses = conn.execute("SELECT * FROM expenses").fetchall()

    conn.close()

    return jsonify([dict(e) for e in expenses])


# ADD EXPENSE
@app.route("/add-expense", methods=["POST"])
def add_expense():

    data = request.get_json()

    item = data["item"]
    amount = data["amount"]
    date = data["date"]

    conn = get_db()

    conn.execute(
        "INSERT INTO expenses(item,amount,date) VALUES (?,?,?)",
        (item, amount, date)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added"})


# DELETE EXPENSE
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_expense(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


# CHART DATA
@app.route("/chart-data")
def chart_data():

    conn = get_db()

    items = conn.execute("""
        SELECT item, SUM(amount) as total
        FROM expenses
        GROUP BY item
    """).fetchall()

    item_labels = [row["item"] for row in items]
    item_values = [row["total"] for row in items]

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
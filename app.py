from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json

app = Flask(__name__)

# SQLite database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route to view all expenses and the main page
@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

# Route to add an expense
@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = request.form['amount']
    description = request.form.get('description', '')
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (category, amount, description) VALUES (?, ?, ?)',
                   (category, float(amount), description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to delete an expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to get the data for the pie chart
@app.route('/chart_data')
def chart_data():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()
    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]
    return jsonify({'categories': categories, 'amounts': amounts})

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(debug=True)

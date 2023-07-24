# this line imports functionality into our projects, so we 
# don't need to write it ourselves!
from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

items = []

db_path = 'checklist.db'

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS checklist
              (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
    conn.commit()
    conn.close()

def get_items():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM chceklist")
    items = c.fetchall()
    conn.close()
    return items

def add_item(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO checklist (item) ALUES (?)", (item,))
    conn.commit()
    conn.close()

def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id))

@app.route('/')
def checklist():
    return render_template('checklist.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item = request.form['item']
    items.append(item)  # Append the new item to the list (not stored in a database)
    return redirect('/')

# now, we're creating the Update functionality/endpoint
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = items[item_id - 1]  # Retrieve the item based on its index in the list (not updated in a database)

    if request.method == 'POST':
        new_item = request.form['item']
        items[item_id - 1] = new_item  # Update the item in the list (not stored in a database)
        return redirect('/')

    return render_template('edit.html', item=item, item_id=item_id)

# Delete
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    del items[item_id - 1]  # Delete the item from the list (not stored in a database)
    return redirect('/')
from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os
import qrcode

app = Flask(__name__)

# Ensure the templates and static directories exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

CSV_PATH = "../data/users.csv"

def ensure_csv_exists():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=['Full Name', 'Staff Number', 'Staff Cadre', 'Meal Type', 'Date Added'])
        df.to_csv(CSV_PATH, index=False)

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save('static/qr_code.png')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'Full Name': request.form['full_name'],
        'Staff Number': request.form['staff_number'],
        'Staff Cadre': request.form['staff_cadre'],
        'Meal Type': request.form['meal_type'],
        'Date Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    ensure_csv_exists()
    # Generate QR code for the local server
    generate_qr_code('http://localhost:5000')
    app.run(host='0.0.0.0', debug=True)

# In the ensure_storage_exists method:
cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        staff_number TEXT NOT NULL,
        staff_cadre TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        date_added TEXT NOT NULL
    )
''')
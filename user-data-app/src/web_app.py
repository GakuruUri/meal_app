from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import qrcode

load_dotenv()

# Create necessary directories
BASE_DIR = os.path.dirname(__file__)  # Changed to use src directory as base
DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')  # Templates will be in src/templates

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
# No need to create templates directory since it already exists

app = Flask(__name__, 
           template_folder=TEMPLATES_DIR,  # Explicitly tell Flask where to find templates
           static_folder=STATIC_DIR)       # Explicitly tell Flask where to find static files

# Use absolute path for CSV file
CSV_PATH = os.path.join(DATA_DIR, 'users.csv')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Add Excel file path and read staff data
STAFF_EXCEL = os.path.join(DATA_DIR, 'document.xlsx')
staff_df = pd.read_excel(STAFF_EXCEL)
print("Excel columns:", staff_df.columns.tolist())  # Debug line to see column names

def ensure_csv_exists():
    """Create CSV file if it doesn't exist"""
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
    full_name = request.form['full_name']
    staff_number = request.form['staff_number']
    
    # Assuming your Excel columns might be named differently
    name_column = 'Name'  # Update this to match your Excel column name
    number_column = 'Staff Number'  # Update this to match your Excel column name
    
    # Check if staff exists and details match
    staff_match = staff_df[
        (staff_df[name_column].str.lower() == full_name.lower()) & 
        (staff_df[number_column] == staff_number)
    ]
    
    if staff_match.empty:
        return render_template('form.html', 
                            error="Invalid staff details. Please check your name and staff number.",
                            full_name=full_name,
                            staff_number=staff_number)
    
    # If match found, proceed with form submission
    data = {
        'Full Name': full_name,
        'Staff Number': staff_number,
        'Staff Cadre': request.form['staff_cadre'],
        'Meal Type': request.form['meal_type'],
        'Date Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    ensure_csv_exists()
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    ensure_csv_exists()
    # Generate QR code for local network URL
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    app_url = f'http://{local_ip}:{PORT}'
    generate_qr_code(app_url)
    print(f"Server running at: {app_url}")
    print(f"QR Code generated for: {app_url}")
    app.run(host=HOST, port=PORT, debug=False)

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
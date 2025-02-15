import pandas as pd
from datetime import datetime
import os
import sqlite3

class StaffDataCollector:
    def __init__(self):
        self.csv_path = "../data/users.csv"
        self.db_path = "../data/staff.db"
        self.ensure_storage_exists()

    def ensure_storage_exists(self):
        """Create CSV file and SQLite database if they don't exist"""
        # Ensure CSV exists
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame(columns=['Full Name', 'Staff Number', 'Staff Cadre', 'Date Added'])
            df.to_csv(self.csv_path, index=False)

        # Ensure SQLite database exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                staff_number TEXT NOT NULL,
                staff_cadre TEXT NOT NULL,
                date_added TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def validate_input(self, prompt, field_name):
        """Validate user input to ensure it's not empty"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print(f"{field_name} cannot be empty!")

    def collect_data(self):
        """Collect staff information from user"""
        print("\n=== Staff Data Collection Form ===\n")
        
        full_name = self.validate_input("Enter Full Name: ", "Full Name")
        staff_number = self.validate_input("Enter Staff Number: ", "Staff Number")
        staff_cadre = self.validate_input("Enter Staff Cadre: ", "Staff Cadre")
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            'Full Name': full_name,
            'Staff Number': staff_number,
            'Staff Cadre': staff_cadre,
            'Date Added': date_added
        }

    def save_data(self, data):
        """Save staff data to both SQLite and CSV"""
        # Save to SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO staff (full_name, staff_number, staff_cadre, date_added)
            VALUES (?, ?, ?, ?)
        ''', (data['Full Name'], data['Staff Number'], data['Staff Cadre'], data['Date Added']))
        conn.commit()
        conn.close()

        # Save to CSV
        df = pd.read_csv(self.csv_path)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(self.csv_path, index=False)
        
        print("\nData successfully saved to both SQLite and CSV!")

    def export_to_csv(self):
        """Export all SQLite data to CSV"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT full_name, staff_number, staff_cadre, date_added FROM staff"
        df = pd.read_sql_query(query, conn)
        df.to_csv(self.csv_path, index=False)
        conn.close()
        print("\nData exported to CSV successfully!")

def main():
    collector = StaffDataCollector()
    
    while True:
        data = collector.collect_data()
        collector.save_data(data)
        
        choice = input("\nWould you like to add another staff member? (y/n): ").lower()
        if choice != 'y':
            break

    # Export final data to CSV
    collector.export_to_csv()
    print("\nThank you for using Staff Data Collector!")

if __name__ == "__main__":
    main()
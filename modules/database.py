import sqlite3

DB_PATH = "database/data/medtrack.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Medicines Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dosage TEXT,
        time TEXT,
        frequency TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)
    try:
      cursor.execute("""
        ALTER TABLE medicines
        ADD COLUMN total_tablets INTEGER DEFAULT 0
    """)
    except sqlite3.OperationalError:
       pass

    try:
        cursor.execute("""
            ALTER TABLE medicines
            ADD COLUMN remaining_tablets INTEGER DEFAULT 0
    """)
    except sqlite3.OperationalError:
       pass

    try:
       cursor.execute("""
        ALTER TABLE medicines
        ADD COLUMN image_path TEXT
    """)
    except sqlite3.OperationalError:
      pass

    # History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_name TEXT,
        dosage TEXT,
        date TEXT,
        time TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_medicine(name, dosage, time, frequency,total_tablets,image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO medicines (name, dosage, time, frequency, status,total_tablets,remaining_tablets,image_path)
    VALUES (?, ?, ?, ?, ? , ? ,? ,?)
    """, (name, dosage, time, frequency, "Pending",total_tablets,total_tablets,image_path))

    conn.commit()
    conn.close()


create_table() 
 
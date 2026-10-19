import sqlite3


def create_table():
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def save_feedback(issue, description):
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO feedback (issue, description) VALUES (?, ?)",
        (issue, description)
    )

    connection.commit()
    connection.close()

def get_all_feedback():
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, issue, description, created_at FROM feedback ORDER BY id DESC"
    )

    records = cursor.fetchall()

    connection.close()

    return records

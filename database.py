import sqlite3



def create_table():
    connection = sqlite3.connect("campuscare.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            description TEXT NOT NULL,
            suggested_category TEXT DEFAULT 'Other',
            suggested_priority TEXT DEFAULT 'Normal',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(feedback)")
    columns = [column[1] for column in cursor.fetchall()]

    if "suggested_category" not in columns:
        cursor.execute(
            "ALTER TABLE feedback ADD COLUMN suggested_category TEXT DEFAULT 'Other'"
        )

    
    if "suggested_priority" not in columns:
        cursor.execute(
            "ALTER TABLE feedback ADD COLUMN suggested_priority TEXT DEFAULT 'Normal'"
        )


    connection.commit()
    connection.close()




def save_feedback(issue, description, suggested_category, suggested_priority):
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (
            issue,
            description,
            suggested_category,
            suggested_priority
        )
        VALUES (?, ?, ?, ?)
        """,
        (issue, description, suggested_category, suggested_priority)
    )

    connection.commit()
    connection.close()




def get_all_feedback():
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute(
        
    cursor.execute(
        """
        SELECT
            id,
            issue,
            description,
            suggested_category,
            suggested_priority,
            created_at
        FROM feedback
        ORDER BY id DESC
        """
    )

    )

    records = cursor.fetchall()

    connection.close()

    return records





def get_feedback_category_counts():
    connection = sqlite3.connect("campuscare.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT suggested_category, COUNT(*)
        FROM feedback
        GROUP BY suggested_category
        ORDER BY COUNT(*) DESC
        """
    )

    category_counts = cursor.fetchall()

    connection.close()

    return category_counts


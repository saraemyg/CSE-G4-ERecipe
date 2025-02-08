import sqlite3
from os import path

def get_db():
    conn = sqlite3.connect('instance/database2.db')
    conn.row_factory = sqlite3.Row
    return conn

class Report:
    @staticmethod
    def get_all_reports():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM report 
                ORDER BY reportTime DESC 
                LIMIT 5
            """)
            reports = cursor.fetchall()
            conn.close()
            return reports
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def update_report_status(report_id, new_status):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE report 
                SET reportStatus = ? 
                WHERE reportID = ?
            """, (new_status, report_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False


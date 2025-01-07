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

class Notification:
    @staticmethod
    def get_all_notifications():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT notiID, notiTime, notiTitle, notiDetails, notiReceiver 
                FROM notification 
                ORDER BY notiTime DESC
            """)
            notifications = cursor.fetchall()
            conn.close()
            return notifications
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def get_notification_by_id(noti_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notification WHERE notiID = ?", (noti_id,))
            notification = cursor.fetchone()
            conn.close()
            return notification
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def add_notification(title, details, receiver):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notification (notiTitle, notiDetails, notiReceiver) 
                VALUES (?, ?, ?)""", (title, details, receiver))
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def update_notification(noti_id, title, details, receiver):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notification 
                SET notiTitle = ?, notiDetails = ?, notiReceiver = ? 
                WHERE notiID = ?""", (title, details, receiver, noti_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def delete_notification(noti_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notification WHERE notiID = ?", (noti_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
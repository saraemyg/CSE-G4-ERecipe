import sqlite3

def get_db():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class RegisteredUser:
    @staticmethod
    def get_all_users():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ru.*, p.userBio, p.userProfilePic, p.userHeaderPic
                FROM registeredUser ru
                LEFT JOIN profile p ON ru.userID = p.userID
            """)
            users = cursor.fetchall()
            conn.close()
            return users
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ru.*, p.userBio, p.userProfilePic, p.userHeaderPic
                FROM registeredUser ru
                LEFT JOIN profile p ON ru.userID = p.userID
                WHERE ru.userID = ?
            """, (user_id,))
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def update_user_status(user_id, new_status):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE registeredUser 
                SET userStatus = ? 
                WHERE userID = ?""", (new_status, user_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
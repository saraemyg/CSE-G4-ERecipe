import sqlite3

def get_db():
    conn = sqlite3.connect('instance/database2.db')
    conn.row_factory = sqlite3.Row
    return conn

class RegisteredUser:
    @staticmethod
    def get_all_users():
        try:
            conn = get_db()
            cursor = conn.cursor()
            # Simplified query for combined table
            cursor.execute("""
                SELECT *
                FROM user
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
                SELECT *
                FROM user
                WHERE userID = ?
            """, (user_id,))
            user = cursor.fetchone()
            conn.close()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        
    @staticmethod
    def get_recipes_by_user_id(user_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM recipe
                WHERE userID = ?
            """, (user_id,))
            recipes = cursor.fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        
    @staticmethod
    def delete_user(user_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE userID = ?", (user_id,))
            conn.commit()  # Commit the changes to the database
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def get_user_by_credentials(username, password):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE userName = ? AND userPassword = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user
        
    @staticmethod
    def get_user_by_username(username):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE userName = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def add_user(username, password, email):
        try:
            conn = get_db()
            cursor = conn.cursor()
            print("Database connection established.")
            cursor.execute("""
                INSERT INTO user (userName, userPassword, userEmail, userPackage, userStatus, userBio, userProfilePic, userHeaderPic)
                VALUES (?, ?, ?, 'free', 'active', '', '', '')
            """, (username, password, email))
            conn.commit()
            print("User added successfully.")
            return True
        
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
                print("Datavase connection closed.")
        
    @staticmethod
    def update_user(user_id, updated_user):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user
                SET userName = ?, userBio = ?, userEmail = ?, userProfilePic = ?, userHeaderPic = ?
                WHERE userID = ?""", (
                    updated_user.get('userName'),
                    updated_user.get('userBio'),
                    updated_user.get('userEmail'),
                    updated_user.get('userProfilePic'),
                    updated_user.get('userHeaderPic'),
                    user_id
                ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
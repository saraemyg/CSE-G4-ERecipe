import sqlite3

def get_db():
    """Returns a database connection."""
    conn = sqlite3.connect('instance/database2.db')
    conn.row_factory = sqlite3.Row
    return conn

class Collection:
    @staticmethod
    def get_all_collections():
        """Fetches all collections from the database."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT collectionID, collectionName, collectionPic FROM collections")
            collections = cursor.fetchall()
            conn.close()
            return collections
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    @staticmethod
    def get_collection_by_id(collection_id):
        """Fetches a single collection by its ID."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collections WHERE collectionID = ?", (collection_id,))
            collection = cursor.fetchone()
            conn.close()
            return collection
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def create_collection(name, description, user_id):
        """Inserts a new collection into the database."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collections (name, description, user_id) 
                VALUES (?, ?, ?)
            """, (name, description, user_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    @staticmethod
    def update_collection(collection_id, name, description):
        """Updates an existing collection."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE collections 
                SET name = ?, description = ?
                WHERE collectionID = ?
            """, (name, description, collection_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def delete_collection(collection_id):
        """Deletes a collection from the database."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM collections WHERE collectionID = ?", (collection_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def get_collections_by_user_id(user_id):
        """Fetch collections for a specific user."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM collection
                WHERE userID = ?
            """, (user_id,))
            collections = cursor.fetchall()
            conn.close()
            return collections
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def get_collection_pic(collection_id):
        """Fetch the first recipe image for a given collection."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.recipePic 
                FROM recipe r
                INNER JOIN collection c ON r.recipeID = c.recipeID
                WHERE c.collectionID = ?
                ORDER BY r.recipeID ASC LIMIT 1
            """, (collection_id,))
            result = cursor.fetchone()
            conn.close()
            return result['recipePic'] if result else 'https://i.pinimg.com/736x/cf/80/06/cf8006f5593281fe559838256b8fb161.jpg/'
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 'https://i.pinimg.com/736x/cf/80/06/cf8006f5593281fe559838256b8fb161.jpg'
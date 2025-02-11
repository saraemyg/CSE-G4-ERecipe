import sqlite3

def get_db():
    """Returns a database connection."""
    conn = sqlite3.connect('instance/database2.db')
    conn.row_factory = sqlite3.Row
    return conn

class Collection:

    @staticmethod
    def get_collections_by_user_id(user_id):
        """Fetch collections with size and image for a specific user."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.collectionID, c.collectionName, 
                    COUNT(r.recipeID) AS collectionSize, 
                    COALESCE(MIN(r.recipePic), 'https://i.pinimg.com/474x/c3/9c/56/c39c56bc405dde5bfd4a92cfdb22f4fd.jpg') AS collectionPic
                FROM collection c
                LEFT JOIN recipe r ON c.recipeID = r.recipeID
                WHERE c.userID = ?
                GROUP BY c.collectionID, c.collectionName
            """, (user_id,))

            collections = cursor.fetchall()
            conn.close()
            return collections
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def get_recipes_by_collection(collection_id):
        """Fetch recipes for a specific collection using a junction table."""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Get all recipeIDs for this collection
            cursor.execute("""
                SELECT r.recipeID, r.recipeTitle, r.recipeDescription, 
                    r.recipePic, r.recipeTime, r.recipeCalories, r.recipeCuisine
                FROM collection c
                JOIN recipe r ON c.recipeID = r.recipeID
                WHERE c.collectionID = ?
            """, (collection_id,))

            recipes = cursor.fetchall()
            conn.close()

            # Return formatted recipe details
            return [
                {
                    'recipeID': row[0],
                    'recipeTitle': row[1],
                    'recipeDescription': row[2],
                    'recipePic': row[3],
                    'recipeTime': row[4],
                    'recipeCalories': row[5],
                    'recipeCuisine': row[6]
                }
                for row in recipes
            ]

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def create_collection(user_id, collection_name):
        """Create a new collection with a manually managed collectionID."""
        try:
            conn = get_db()
            cursor = conn.cursor()

            # Fetch the highest current collectionID and increment it
            cursor.execute("SELECT COALESCE(MAX(collectionID), 0) FROM collection")
            max_id = cursor.fetchone()[0]
            new_collection_id = max_id + 1

            # Insert the new collection
            cursor.execute("""
                INSERT INTO collection (collectionID, collectionName, userID)
                VALUES (?, ?, ?)
            """, (new_collection_id, collection_name, user_id))

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def add_recipe_to_collection(collection_id, recipe_id):
        """Add a recipe to a collection."""
        try:
            conn = get_db()
            cursor = conn.cursor()

            # Check if the recipe is already in the collection
            cursor.execute("SELECT * FROM collection WHERE collectionID = ? AND recipeID = ?", (collection_id, recipe_id))
            existing = cursor.fetchone()

            if existing:
                print("Recipe already exists in this collection.")
                return False  # Prevent duplicates

            cursor.execute("""
                INSERT INTO collection (collectionID, recipeID)
                VALUES (?, ?)
            """, (collection_id, recipe_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
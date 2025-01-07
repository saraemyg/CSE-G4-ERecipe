import sqlite3

def get_db():
    conn = sqlite3.connect('instance/database2.db')
    conn.row_factory = sqlite3.Row
    return conn

class Recipe:
    @staticmethod
    def get_all_recipes():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipe")
            recipes = cursor.fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    @staticmethod
    def get_recipe_by_id(recipe_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipe WHERE recipeID = ?", (recipe_id,))
            recipe = cursor.fetchone()
            conn.close()
            return recipe
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @staticmethod
    def update_recipe_status(recipe_id, new_status):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE recipe 
                SET recipeStatus = ? 
                WHERE recipeID = ?""", (new_status, recipe_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
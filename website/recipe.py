import sqlite3
from .models import DatabaseManager

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
    def get_recipe_by_user_id(user_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipe WHERE userID = ?", (user_id,))
            recipes = cursor.fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

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
        
    @staticmethod
    def get_recipe_like_count(recipe_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM `like` WHERE recipeID = ?", (recipe_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0  # result[0] holds the like count
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

    @staticmethod
    def suspend_recipe(recipe_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE recipe SET recipeStatus = 'suspended' WHERE recipeID = ?", (recipe_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete_recipe(recipe_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipe WHERE recipeID = ?", (recipe_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def search_recipe(query):
        db = DatabaseManager.get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT recipeID, recipeTitle, recipePic, recipeDescription, recipeTime, recipeCalories, recipeCuisine
            FROM recipe
            WHERE recipeTitle LIKE ? OR recipeDescription LIKE ?
        """, (f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()

        recipe = [
            {
                "recipeID": row[0],
                "recipeTitle": row[1],
                "recipePic": row[2],
                "recipeDescription": row[3],
                "recipeTime": row[4],
                "recipeCalories": row[5],
                "recipeCuisine": row[6]
            }
            for row in results
        ]

        return recipe

    @staticmethod
    def get_published_recipes():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipe WHERE recipeStatus = 'published'")
            recipes = cursor.fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
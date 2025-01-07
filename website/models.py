import sqlite3
from os import path
import os

DB_NAME = "database2.db"
DB_PATH = path.join('instance', DB_NAME)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class DatabaseManager:
    @staticmethod
    def init_db():
        # if not path.exists(DB_PATH):
        #     conn = get_db()
        #     cursor = conn.cursor()
        os.makedirs('instance', exist_ok=True)

        try:
            conn = get_db()
            cursor = conn.cursor()

            cursor.executescript("""
                -- Drop existing tables in reverse order
                DROP TABLE IF EXISTS report;
                DROP TABLE IF EXISTS recipe;
                DROP TABLE IF EXISTS notification;
                DROP TABLE IF EXISTS registeredUser;

                -- Create tables in correct order
                CREATE TABLE registeredUser (
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    userName TEXT NOT NULL UNIQUE,
                    userPassword TEXT NOT NULL,
                    userEmail TEXT NOT NULL UNIQUE,
                    userPackage TEXT NOT NULL,
                    userStatus TEXT NOT NULL,
                    userBio TEXT,
                    userProfilePic TEXT,
                    userHeaderPic TEXT
                );

                CREATE TABLE notification (
                    notiID INTEGER PRIMARY KEY AUTOINCREMENT,
                    notiTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notiTitle TEXT NOT NULL,
                    notiDetails TEXT NOT NULL,
                    notiReceiver TEXT NOT NULL,
                    FOREIGN KEY (notiReceiver) REFERENCES registeredUser(userPackage)
                );

                CREATE TABLE recipe (
                    recipeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipeTitle TEXT NOT NULL,
                    recipeDescription TEXT NOT NULL,
                    recipeIngredients TEXT NOT NULL,
                    recipeSteps TEXT NOT NULL,
                    recipePic TEXT,
                    recipeTime INTEGER NOT NULL,
                    recipeCalories INTEGER NOT NULL,
                    recipeLabel TEXT,
                    recipeCuisine TEXT,
                    recipeStatus TEXT NOT NULL,
                    userID INTEGER NOT NULL,
                    FOREIGN KEY (userID) REFERENCES registeredUser(userID)
                );

                CREATE TABLE report (
                    reportID INTEGER PRIMARY KEY AUTOINCREMENT,
                    reportTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reportStatus TEXT NOT NULL DEFAULT 'pending',
                    reportDetails TEXT NOT NULL,
                    reportSenderUserID INTEGER NOT NULL,
                    reportedRecipeID INTEGER NOT NULL,
                    FOREIGN KEY (reportSenderUserID) REFERENCES registeredUser(userID),
                    FOREIGN KEY (reportedRecipeID) REFERENCES recipe(recipeID)
                );
            """)

            cursor.executemany("""
            INSERT INTO registeredUser (userName, userPassword, userEmail, userPackage, userStatus, userBio, userProfilePic, userHeaderPic) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ('johan_doe', 'hashed_password1', 'john@example.com', 'premium', 'active',
                 'Food enthusiast and home chef. Love experimenting with new recipes and sharing cooking tips.',
                 'https://i.pinimg.com/736x/91/11/0f/91110f54c48f7196cf9af376416aada5.jpg', 
                 'https://i.pinimg.com/736x/02/5a/15/025a156857a5a4784dd6b61e7398bfd2.jpg'),
                ('jane_smith', 'hashed_password2', 'jane@example.com', 'premium', 'active',
                 'Professional baker with 5 years experience. Specializing in pastries and desserts.',
                 'https://i.pinimg.com/736x/a7/14/1d/a7141d860f5e54ac15b40cf5b672e577.jpg', 
                 'https://i.pinimg.com/736x/7f/5e/62/7f5e629664cc372b6d505d8a18682e89.jpg'),
                ('alice_jones', 'hashed_password3', 'alice@example.com', 'free', 'active',
                 'Passionate about healthy cooking and nutrition. Sharing balanced meal recipes.',
                 'https://i.pinimg.com/736x/84/e9/34/84e934bd5d08fbd3ff1ea7e29a69c5ec.jpg', 
                 'https://i.pinimg.com/736x/60/19/de/6019deab1e45a989f37f8f96fffdbf82.jpg'),
                ('bob_wilson', 'hashed_password4', 'bob@example.com', 'premium', 'suspended',
                 'Traditional cuisine lover. Exploring and preserving family recipes.',
                 'https://i.pinimg.com/736x/7e/dd/01/7edd01552dd2d8cbb99b4b967692d50c.jpg', 
                 'https://i.pinimg.com/736x/b0/8c/8d/b08c8d19049319406f3150379a30bb14.jpg'),
                ('emma_davis', 'hashed_password5', 'emma@example.com', 'free', 'active',
                 'Food photographer and recipe developer. Making cooking accessible for everyone.',
                 'https://i.pinimg.com/736x/26/6e/ae/266eae833606799f101cb37f93f0774d.jpg', 
                 'https://i.pinimg.com/736x/a9/5a/04/a95a049c84c4bb80837e49ae551818eb.jpg')
            ])

            cursor.executemany("""
            INSERT INTO notification (notiTitle, notiDetails, notiReceiver) 
            VALUES (?, ?, ?)
            """, [
                ('System Maintenance', 'The system will be down for maintenance from 12 AM to 3 AM.', 'admin'),
                ('New Report Available', 'A new report has been generated and ready for review.', 'manager'),
                ('User Registered', 'A new user has registered on the platform.', 'support'),
                ('Weekly Newsletter', 'The latest newsletter is now available for all subscribers.', 'subscriber')
            ])

            cursor.executemany("""
            INSERT INTO recipe (recipeTitle, recipeDescription, recipeIngredients, recipeSteps, recipePic, recipeTime, recipeCalories, recipeLabel, recipeCuisine, recipeStatus, userID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ('Spaghetti Bolognese', 'A classic Italian pasta dish', 'Spaghetti, Ground Beef, Tomato Sauce, Onions, Garlic, Olive Oil, Salt, Pepper', '1. Cook spaghetti. 2. Prepare sauce. 3. Mix and serve.', 'https://i.pinimg.com/736x/0c/6b/f8/0c6bf8a61e458e4f59b994bf50229534.jpg', 30, 600, 'Dinner, Pasta', 'Italian', 'published', 1),
                ('Chicken Curry', 'A spicy and flavorful chicken curry', 'Chicken, Curry Powder, Coconut Milk, Onions, Garlic, Ginger, Salt, Pepper', '1. Cook chicken. 2. Prepare curry sauce. 3. Mix and serve.', 'https://i.pinimg.com/736x/46/04/f6/4604f69d4efd0d65d10a59260f59ed64.jpg', 45, 700, 'Dinner, Curry', 'Indian', 'published', 2),
                ('Chocolate Cake', 'A rich and moist chocolate cake', 'Flour, Sugar, Cocoa Powder, Baking Powder, Eggs, Milk, Butter, Vanilla Extract', '1. Prepare batter. 2. Bake cake. 3. Frost and serve.', 'https://i.pinimg.com/736x/e9/a7/18/e9a7186766fdb247dfba0d1a8c6c26b7.jpg', 60, 500, 'Dessert, Cake', 'American', 'published', 3),
                ('Sushi Roll', 'Fresh and delicious Japanese sushi', 'Sushi Rice, Nori, Fresh Salmon, Cucumber, Avocado, Rice Vinegar, Wasabi', '1. Prepare rice. 2. Layer ingredients. 3. Roll and cut.', 'https://i.pinimg.com/736x/54/95/f7/5495f7a532a4a9c9fb3861bccf5beaa0.jpg', 40, 350, 'Lunch, Dinner', 'Japanese', 'published', 1),
                ('Pad Thai', 'Classic Thai stir-fried noodles', 'Rice Noodles, Shrimp, Tofu, Bean Sprouts, Peanuts, Tamarind Sauce, Lime', '1. Soak noodles. 2. Stir fry ingredients. 3. Add sauce.', 'https://i.pinimg.com/736x/c5/bd/f2/c5bdf2d9269d436331ea20d8c0269436.jpg', 25, 450, 'Dinner, Noodles', 'Thai', 'published', 2),
                ('Greek Salad', 'Fresh Mediterranean salad', 'Cucumber, Tomatoes, Red Onion, Olives, Feta Cheese, Olive Oil, Oregano', '1. Chop vegetables. 2. Mix ingredients. 3. Add dressing.', 'https://i.pinimg.com/736x/72/14/d1/7214d152bf9eb5561fec0ca4afc23955.jpg', 15, 280, 'Lunch, Salad', 'Greek', 'published', 3),
                ('Beef Tacos', 'Authentic Mexican street tacos', 'Ground Beef, Corn Tortillas, Onion, Cilantro, Lime, Salsa, Spices', '1. Cook beef. 2. Warm tortillas. 3. Assemble tacos.', 'https://i.pinimg.com/736x/32/25/82/322582f81dd43d0cf57502c1d9a7a586.jpg', 20, 400, 'Dinner, Mexican', 'Mexican', 'published', 1),
                ('Vegetable Biryani', 'Aromatic Indian rice dish', 'Basmati Rice, Mixed Vegetables, Yogurt, Saffron, Biryani Spices, Ghee', '1. Cook rice. 2. Prepare vegetables. 3. Layer and steam.', 'https://i.pinimg.com/736x/6a/cc/f3/6accf3cefbe7f9779d151e3696018990.jpg', 55, 550, 'Dinner, Rice', 'Indian', 'published', 2)
            ])

            cursor.executemany("""
            INSERT INTO report (reportStatus, reportDetails, reportSenderUserID, reportedRecipeID) 
            VALUES (?, ?, ?, ?)
            """, [
                ('pending', 'Inappropriate content in recipe description', 1, 1),
                ('resolved', 'Wrong ingredients listed', 2, 2),
                ('pending', 'Copyright violation', 3, 3)
            ])

            conn.commit()
            # conn.close()
            print('Database created successfully!')
        
        except sqlite3.Error as e:
                print(f"Database error: {e}")
                if conn:
                    conn.close()
        finally:
            if conn:
                conn.close()
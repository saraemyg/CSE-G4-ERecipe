from flask import Flask, render_template, redirect, url_for, request, flash, session
from .models import DatabaseManager
from .admin import Report, Notification
from .user import RegisteredUser
from .recipe import Recipe
from .comment import Comment

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'saranadianisafiza'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
    
    DatabaseManager.init_db()

    # ----------------- MAIN ROUTES -----------------
    @app.route("/")
    def main():
        return render_template('main.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        
            user = RegisteredUser.get_user_by_credentials(username, password)
            if user:
                session['user'] = user['userName']
                return redirect(url_for('userhome'))
            else:
                flash('Invalid username or password', 'error')
    
        return render_template('login.html')
    
    @app.route('/user/<int:id>')
    def get_user(id):
        user = RegisteredUser.get_user_by_id(id)
        if user:
            return {
                'userID': user['userID'],  
                'userName': user['userName'],
                'userEmail': user['userEmail'],
                'userBio': user['userBio'],
                'userPackage': user['userPackage'],
                'userHeaderPic': user['userHeaderPic'], 
                'userProfilePic': user['userProfilePic'], 
                'userStatus': user['userStatus']  
            }
        return {'error': 'User  not found'}, 404

    @app.route('/recipe/<int:id>')
    def get_recipe(id):
        recipe = Recipe.get_recipe_by_id(id)
        if recipe:
            like_count = Recipe.get_recipe_like_count(id)  # Fetch the like count
            return {
                'recipeID': recipe['recipeID'],
                'recipeTitle': recipe['recipeTitle'],
                'recipeDescription': recipe['recipeDescription'],
                'recipeIngredients': recipe['recipeIngredients'],
                'recipeSteps': recipe['recipeSteps'],
                'recipePic': recipe['recipePic'],
                'recipeTime': recipe['recipeTime'],
                'recipeCalories': recipe['recipeCalories'],
                'recipeLabel': recipe['recipeLabel'],
                'recipeCuisine': recipe['recipeCuisine'],
                'recipeStatus': recipe['recipeStatus'],
                'userID': recipe['userID'],
                'likeCount': like_count,  # Include the like count in the response
            }
        return {'error': 'Recipe not found'}, 404

    @app.route('/user/<int:id>/recipes')
    def get_user_recipes(id):
        # Fetch user recipes
        recipes = Recipe.get_recipe_by_user_id(id)
        if recipes:
            return {'recipes': [dict(recipe) for recipe in recipes]}  # Return a list of recipes in a JSON-friendly format
        return {'recipes': []}  # If no recipes are found, return an empty list

    @app.route('/recipe/<int:id>/likes')
    def get_recipe_like_count(id):
        # Fetch the total like count for the specified recipe
        like_count = Recipe.get_recipe_like_count(id)
        return {'recipeID': id, 'likeCount': like_count}


    # ----------------- COMMENT ROUTES -----------------
    @app.route('/recipe/<int:id>/comments')
    def get_recipe_comments(id):
        comments = Comment.get_comments_by_recipe_id(id)
        return {
            'comments': [dict(comment) for comment in comments]
        }

    # ----------------- ADMIN ROUTES -----------------
    @app.route('/adminhome')
    def adminhome():
        reports = Report.get_all_reports()
        notifications = Notification.get_all_notifications()
        return render_template('adminhome.html', reports=reports, notifications=notifications)
    
    @app.route('/reports')
    def reports():
        reports = Report.get_all_reports()
        return render_template('adminreport.html', reports=reports)
    
    @app.route('/notifications')
    def notifications():
        notifications = Notification.get_all_notifications()
        return render_template('adminnoti.html', notifications=notifications)
    
    @app.route('/notification/delete/<int:id>', methods=['POST'])
    def delete_notification(id):
        Notification.delete_notification(id)
        return redirect(url_for('notifications'))
    
    @app.route('/notification/edit/<int:id>', methods=['GET', 'POST'])
    def edit_notification(id):
        if request.method == 'POST':
            title = request.form.get('title')
            details = request.form.get('details')
            receiver = request.form.get('receiver')
            Notification.update_notification(id, title, details, receiver)
            return redirect(url_for('notifications'))
        notification = Notification.get_notification_by_id(id)
        return render_template('edit_notification.html', notification=notification)
    
    @app.route('/notification/<int:id>')
    def get_notification(id):
        notification = Notification.get_notification_by_id(id)
        if notification:
            return {
                'title': notification['notiTitle'],
                'details': notification['notiDetails'],
                'receiver': notification['notiReceiver']
            }
        return {'error': 'Notification not found'}, 404
    
    @app.route('/notification/create', methods=['POST'])
    def create_notification():
        if request.method == 'POST':
            title = request.form.get('title')
            details = request.form.get('details')
            receiver = request.form.get('receiver')
            Notification.add_notification(title, details, receiver)
            return redirect(url_for('notifications'))
        
    @app.route('/report/update_status/<int:id>', methods=['POST'])
    def update_report_status(id):
        new_status = request.form.get('status')
        Report.update_report_status(id, new_status)
        return redirect(url_for('reports'))
    
    @app.route('/manage')
    def manage():
        users = RegisteredUser.get_all_users()
        recipes = Recipe.get_all_recipes()
        userDetails = RegisteredUser.get_user_by_id(id)     # check what is this for
        return render_template('adminmanage.html', users=users, recipes=recipes)
    
    @app.route('/recipe/<int:id>/suspend', methods=['POST'])
    def suspend_recipe(id):
        try:
            # Suspend the recipe by updating its status to 'suspended'
            Recipe.suspend_recipe(id)
            flash('Recipe has been suspended successfully.', 'success')
            return redirect(url_for('view_recipe', id=id))  # Redirect to the recipe view page or a manage page
        except Exception as e:
            flash(f'Error suspending recipe: {e}', 'error')
            return redirect(url_for('view_recipe', id=id))  # Handle error and redirect back

    @app.route('/recipe/<int:id>/delete', methods=['POST'])
    def delete_recipe(id):
        try:
            # Delete the recipe from the database
            Recipe.delete_recipe(id)
            flash('Recipe has been deleted successfully.', 'success')
            return redirect(url_for('manage'))  # Redirect to the manage recipes page
        except Exception as e:
            flash(f'Error deleting recipe: {e}', 'error')
            return redirect(url_for('view_recipe', id=id))  # Handle error and redirect back

    
    # ----------------- USER ROUTES -----------------

    @app.route('/userhome')
    def userhome():
        return render_template('userhome.html')
    
    @app.route('/createrecipe')
    def createrecipe():
        return render_template('createrecipe.html')
    
    @app.route('/profile')
    def profile():
        if 'user' not in session:
            return redirect(url_for('login'))
        
        username = session['user']
        user = RegisteredUser.get_user_by_username(username)
        recipes = RegisteredUser.get_recipes_by_user_id(user['userID']) if user else []
        if user:
            return render_template('profile.html', user=user, recipes=recipes)
        else:
            flash('User not found', 'error')
            return redirect(url_for('userhome'))
    
    @app.route('/collection')
    def collection():
        return render_template('collection.html')
    
    # ----------------- -----------------

    return app
from flask import Flask, render_template, redirect, url_for, request, flash, session
from .models import DatabaseManager
from .admin import Admin, Report, Notification
from .user import RegisteredUser
from .recipe import Recipe
from .comment import Comment
from .collection import Collection

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'saranadianisafiza'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
    
    DatabaseManager.init_db()

    # ----------------- MAIN ROUTES -----------------
    @app.route("/")
    def main():
        return render_template('main.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')

            if RegisteredUser.get_user_by_username(username):
                flash('Username already exists', 'error')
                return render_template('login.html')
            
            success = RegisteredUser.add_user(username, password, email)
            if success:
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Signup failed. Try again.', 'error')

        return render_template('login.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Check if the user exists in the user table
            user = RegisteredUser.get_user_by_username(username)
            if user and user['userPassword'] == password:
                session['user'] = user['userName']
                session['role'] = 'user'
                return redirect(url_for('userhome'))

            # If not a user, check if it's an admin
            admin = Admin.get_admin_by_username(username)
            if admin and admin['adminPassword'] == password:
                session['user'] = admin['adminName']
                session['role'] = 'admin'
                return redirect(url_for('adminhome'))

            # Invalid login
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

        return render_template('login.html')

    
    @app.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('role', None)
        return redirect(url_for('main'))
    

    
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
    
    @app.route('/user/username/<string:username>')
    def get_user_by_username(username):
        user = RegisteredUser.get_user_by_username(username)
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
        return {'error': 'User not found'}, 404


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

    # ----------------- LIKE & COMMENT ROUTES -----------------

    @app.route('/recipe/<int:id>/likes')
    def get_recipe_like_count(id):
        # Fetch the total like count for the specified recipe
        like_count = Recipe.get_recipe_like_count(id)
        return {'recipeID': id, 'likeCount': like_count}

    @app.route('/recipe/<int:id>/comments')
    def get_recipe_comments(id):
        comments = Comment.get_comments_by_recipe_id(id)
        return {
            'comments': [dict(comment) for comment in comments]
        }

    # ----------------- ADMIN MANAGE ROUTES -----------------#
    
    @app.route('/adminhome')
    def adminhome():
        if session.get('role') != 'admin':
            return redirect(url_for('login'))
        
        username = session.get('user')  # Assuming the admin username is stored in the session
        admin = Admin.get_admin_by_username(username)
        
        if not admin:
            flash("Admin not found", "error")
            return redirect(url_for('login'))

        reports = Report.get_all_reports()
        notifications = Notification.get_all_notifications()

        return render_template(
            'adminhome.html',
            admin_info={
                'adminID': admin['adminID'],
                'adminName': admin['adminName'],
                'adminEmail': admin['adminEmail'],
                'adminProfilePic': admin['adminProfilePic']
            },
            reports=reports,
            notifications=notifications
        )

    @app.route('/admin/<username>')
    def get_admin(username):
        admin = Admin.get_admin_by_username(username)
        if admin:
            return {
                'adminID': admin['adminID'],
                'adminName': admin['adminName'],
                'adminEmail': admin['adminEmail'],
                'adminProfilePic': admin['adminProfilePic']
            }
        return {"error": "Admin not found"}, 404

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


    # ----------------- REPORT ROUTES -----------------
    @app.route('/reports')
    def reports():
        reports = Report.get_all_reports()
        return render_template('adminreport.html', reports=reports)
    
    @app.route('/report/update_status/<int:id>', methods=['POST'])
    def update_report_status(id):
        new_status = request.form.get('status')
        if not new_status:
            return "Invalid status", 400
        
        Report.update_report_status(id, new_status)
        return redirect(url_for('reports'))

        
    @app.route('/report/<int:report_id>')
    def get_report_details(report_id):
        report = Report.get_report_details(report_id)
        if report:
            return {
                'reportID': report['reportID'],
                'reportDetails': report['reportDetails'],
                'reportTime': report['reportTime'],
                'reportStatus': report['reportStatus'],
                'reportedUser': report['reportedUser'],
                'reportSenderUser': report['reportSenderUser'],
                'relatedRecipe': report['relatedRecipe']
            }
        return {'error': 'Report not found'}, 404

    # ----------------- NOTIFICATION ROUTES -----------------
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
    
    # ----------------- USER ROUTES -----------------

    @app.route('/userhome')
    def userhome():
        recipes = Recipe.get_all_recipes()
        notifications = Notification.get_all_notifications()
        return render_template('userhome.html', recipes=recipes,  notifications=notifications)
    
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
        
    @app.route('/profile/edit', methods=['GET', 'POST'])
    def edit_profile():
        if 'user' not in session:
            return redirect(url_for('login'))
        
        username = session['user']
        user = RegisteredUser.get_user_by_username(username)
        if request.method == 'POST':
            email = request.form.get('email')
            bio = request.form.get('bio')
            package = request.form.get('package')
            header_pic = request.form.get('header_pic')
            profile_pic = request.form.get('profile_pic')
            RegisteredUser.update_user(user['userID'], email, bio, package, header_pic, profile_pic)
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', user=user)
    

    
    # ----------------- COLLECTION ROUTES -----------------

    @app.route('/collection')
    def collection():
        username = session.get('user')
        if not username:
            flash('Please log in to access your collections.', 'warning')
            return redirect(url_for('login'))

        user = RegisteredUser.get_user_by_username(username)
        if user:
            user_id = user['userID']
            collections = Collection.get_collections_by_user_id(user_id)
            
            # Fetch collection data with the first recipe image
            formatted_collections = [
                {
                    'collectionID': collection['collectionID'],
                    'collectionName': collection['collectionName'],
                    'collectionPic': Collection.get_collection_pic(collection['collectionID'])
                }
                for collection in collections
            ]

            return render_template('collection.html', collections=formatted_collections)

        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('login'))

    # ----------------- -----------------

    return app
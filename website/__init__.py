from flask import Flask, render_template, redirect, url_for, request, flash
from .models import DatabaseManager
from .admin import Report, Notification
from .user import RegisteredUser
from .recipe import Recipe

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'saranadianisafiza'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
    
    DatabaseManager.init_db()

    # ----------------- MAIN ROUTES -----------------
    @app.route("/")
    def main():
        return render_template('main.html')
    
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
                'userID': recipe['userID']
            }
        return {'error': 'Recipe not found'}, 404

    @app.route('/logout')
    def logout():
        return redirect(url_for('home'))

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
    
    @app.route('/user/suspend/<int:id>', methods=['POST'])
    def suspend_user(id):
        # Logic to suspend the user
        user = RegisteredUser .get_user_by_id(id)
        if user:
            # Assuming you have a method to suspend the user
            RegisteredUser .suspend_user(id)
            return '', 204  # No content response
        return {'error': 'User  not found'}, 404

    @app.route('/user/delete/<int:id>', methods=['POST'])
    def delete_user(id):
        RegisteredUser .delete_user(id)  # Implement this method in your RegisteredUser  class
        return redirect(url_for('manage'))  # Redirect to the manage page or wherever appropriate
    
    # ----------------- USER ROUTES -----------------


    @app.route('/userhome')
    def userhome():
        return render_template('userhome.html')
    
    @app.route('/createrecipe')
    def createrecipe():
        return render_template('createrecipe.html')
    
    @app.route('/profile')
    def profile():
        return render_template('profile.html')
    
    # ----------------- -----------------

    return app
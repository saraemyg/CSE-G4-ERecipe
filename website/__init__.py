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

    @app.route('/')
    def adminhome():
        reports = Report.get_all_reports()
        notifications = Notification.get_all_notifications()
        return render_template('adminhome.html', reports=reports, notifications=notifications)
    
    @app.route('/notifications')
    def notifications():
        notifications = Notification.get_all_notifications()
        return render_template('adminnoti.html', notifications=notifications)
    
    @app.route('/reports')
    def reports():
        reports = Report.get_all_reports()
        return render_template('adminreport.html', reports=reports)
    
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
        return render_template('adminmanage.html', users=users, recipes=recipes)
    
    @app.route('/logout')
    def logout():
        return redirect(url_for('home'))
    
    return app
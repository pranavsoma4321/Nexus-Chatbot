from flask import Flask, render_template, redirect, url_for, flash, request, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Change this in production

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Create database tables
with app.app_context():
    db.create_all()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login Route
@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handle login requests"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    
    return render_template("login.html")

# Signup Route
@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    """Handle signup requests"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('signup_page'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup_page'))
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup_page'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('signup_page'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account', 'error')
            return redirect(url_for('signup_page'))
    
    return render_template("signup.html")

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('signup_page'))

# Home / Index Route - Redirect to signup if not logged in
@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('signup_page'))
    username = session.get('username', 'Guest')
    return render_template("home.html", username=username)

@app.route("/home")
def home():
    username = session.get('username', 'Guest')
    return render_template("home.html", username=username)

# Customize Upload Page
@app.route("/customize_upload")
def customize_upload():
    username = session.get('username', 'Guest')
    return render_template("customize_upload.html", username=username)

# Choose Model Page
@app.route("/choose_model")
def choose_model():
    username = session.get('username', 'Guest')
    return render_template("choose_model.html", username=username)

@app.route("/customize_chatbot")
def customize_chatbot():
    username = session.get('username', 'Guest')
    return render_template("customize_chatbot.html", username=username)

@app.route("/bot_builder")
def bot_builder():
    username = session.get('username', 'Guest')
    return render_template("bot_builder.html", username=username)

# Bot Templates Page
@app.route("/templates")
def templates():
    username = session.get('username', 'Guest')
    return render_template("templates.html", username=username)

# My Bots Dashboard
@app.route("/my_bots")
def my_bots():
    username = session.get('username', 'Guest')
    return render_template("my_bots.html", username=username)

# Assignments Page
@app.route("/assignments")
def assignments():
    username = session.get('username', 'Guest')
    return render_template("assignments.html", username=username)

# Assignment Detail Page
@app.route("/assignment/<assignment_id>")
def assignment_detail(assignment_id):
    username = session.get('username', 'Guest')
    return render_template("assignment_detail.html", username=username, assignment_id=assignment_id)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ben_chow_secret_key' # Needed for flash messages

# 2. Initialize Database
db = SQLAlchemy(app) 

# 3. User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# 4. Create Tables
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    # If index.html doesn't exist yet, you can use: return redirect(url_for('login'))
    return render_template('index.html')

from flask import session # Make sure to add session to your imports

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('email')
        login_password = request.form.get('password')

        user = User.query.filter_by(email=login_email).first()

        if user and user.password == login_password:
            # SAVE THE NAME HERE
            session['user_name'] = user.name 
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        # Check if email already exists to avoid errors
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            flash("Email already registered!", "warning")
            return redirect(url_for('register'))

        new_user = User(name=new_name, email=new_email, password=new_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Get the name from session, use 'Guest' if not found
    name = session.get('user_name', 'Lecturer') 
    return render_template('dashboard.html', name=name)

@app.route('/logout')
def logout():
    session.pop('user_name', None) # This "forgets" the name
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# 5. Start the Server (Must be the very last thing!)
if __name__ == '__main__':
    app.run(debug=True)
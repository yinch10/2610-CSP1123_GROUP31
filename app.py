from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Initialize SQLAlchemy with the app
db = SQLAlchemy(app) 

# 3. Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# 4. Create the database tables
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('email')
        login_password = request.form.get('password')

        user = User.query.filter_by(email=login_email).first()

        # ADD THIS LINE TO DEBUG:
        print(f"Login Attempt: {login_email}, Found User: {user}")

        if user and user.password == login_password:
            return redirect(url_for('home'))
        # ... rest of your code

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        new_user = User(name=new_name, email=new_email, password=new_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

# 5. Start the Server
if __name__ == '__main__':
    app.run(debug=True)
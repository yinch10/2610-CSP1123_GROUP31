from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. Home Route
@app.route('/')
def home():
    return render_template('index.html')

# 2. Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logical check will go here later
        return redirect(url_for('home'))
    return render_template('login.html')

# 3. Start the Server (Must always be at the bottom!)
if __name__ == '__main__':
    app.run(debug=True)
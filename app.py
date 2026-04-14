from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # This looks inside the 'templates' folder for your file
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
# We will add Flask-Login later, for now just render the page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # This is where your logic will go later to check passwords
        return redirect(url_for('home'))
    return render_template('login.html')
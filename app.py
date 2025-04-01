from flask import Flask, render_template, request, redirect, url_for, session, flash

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# In-memory user storage (replace with database in production)
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        users[username] = password
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users or users[username] != password:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        
        session['username'] = username
        flash('Login successful!')
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

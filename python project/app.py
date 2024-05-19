from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Dummy user credentials (replace with a proper authentication mechanism)
users = {'user1': 'matcya', 'user2': 'team'}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('welcome', username=session['username']))
    return render_template('login.html', error=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        # Authentication successful, store username in session and redirect to welcome page
        session['username'] = username
        return redirect(url_for('welcome', username=username))
    else:
        # Authentication failed, redirect back to login page with an error message
        return render_template('login.html', error=True)

@app.route('/welcome/<username>')
def welcome(username):
    if 'username' in session and session['username'] == username:
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

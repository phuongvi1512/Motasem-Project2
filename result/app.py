from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
USER_INFO = {
    "username": "admin",
    "password": "password"
}


# client = MongoClient("mongodb://mongodb:27017")

# db = client['analyticdb']
# collection = db['analytic']

@app.route('/')
def home():
    return render_template('home.html')
#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_INFO['username'] and password == USER_INFO['password']:
            session['logged_in'] = True
            flash('You were just logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    #connect to mongodb analyticdb and collection analytic and retrieve all data number of reports, max size, avg size and timestamp
    #redirect to login page if not logged in
    if not session.get('logged_in'):
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    try:
        client = MongoClient(
            host=os.getenv('MONGODB_HOST'),
            port=int(os.getenv('MONGODB_PORT')))
        db = client['analyticdb']
        collection = db['analytic']

        data = list(collection.find())
        #print(data)
        return render_template('dashboard.html', data=data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002)
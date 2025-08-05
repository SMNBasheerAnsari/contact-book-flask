from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Contact, User # import db and models
import requests
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'afeaf920556d9624048688836237a8c4' 

# Init DB and Login Manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route - View all contacts
@app.route('/')
@login_required
def index():
    contacts=Contact.query.all()
    return render_template('index.html',contacts = contacts )

# Add new contact route
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name= request.form['name']
        phone= request.form['phone']
        email= request.form['email']
        address=request.form['address']
        dob=request.form['dob']
        
        if not name or not phone:
            flash("Name and Phone are mandatory.")
            return redirect(url_for('add_contact'))

        contact = Contact(name=name, phone=phone, email=email, address=address, dob=dob)
        db.session.add(contact)
        db.session.commit()
        flash("Contact added successfully!")
        return redirect(url_for('index'))
    return render_template('add.html')

# Signup
@app.route('/singup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email, password=password, role='user')
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful. Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('login'))
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

'''
contacts=[] # in-memory storage list for contacts as a doctionary 

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        dob = request.form['dob']

        contacts.append({
            'name':name, 
            'phone': phone, 
            'email': email,
            'address': address,
            'dob': dob      })

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete_contact(index):
    if 0 <= index < len(contacts):
        del contacts[index]
    return redirect(url_for('index'))
'''

if __name__ == '__main__':
    app.run(debug=True)

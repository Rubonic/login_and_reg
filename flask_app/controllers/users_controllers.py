from flask_app import app
from flask import render_template, redirect, request, session
from flask import flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                            # which is made by invoking the function Bcrypt with our app as an argument



@app.route('/')
def index():

    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    #1. validate the form
    if not User.validate_user_registration(request.form):
        return redirect('/')
    #2. create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #3 put hash into data dictionary
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.create(data)

    session['user_id'] = user_id
    
    return redirect(f'/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)
    # user is not registered in the db
    if not user:
        flash("Invalid Email/Password", 'login')
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    # never render on a post!!!
    return redirect("/dashboard/")


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Please login or register before proceeding', 'login')
        return redirect('/')

    data = { 'user_id' : session['user_id']}
    user = User.get_user(data)

    return render_template('dashboard.html', user = user)


@app.route('/clear_session')
def clear_session():
    session.clear()

    return redirect('/')


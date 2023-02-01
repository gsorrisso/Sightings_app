from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/')
def login_page():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_registration(request.form):
        return redirect('/') # you had this redirecting to log out but it was letting the flash messages pop up.. so keep it at redirect home

    User.save( 
        {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']),
        }
    )
    user = User.get_email(
        {
            'email': request.form['email']
        }
    )
    session['user_id'] = user.id

    return redirect('/profile_page')



@app.route('/user/login', methods=['POST'])
def login():
    
    user = User.get_email(
        {'email': request.form['email']}
    )

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Credentials", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    # has to do credential check before using session key note!
    return redirect('/profile_page')


@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')



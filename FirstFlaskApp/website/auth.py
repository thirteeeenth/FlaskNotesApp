# we will create another routes blueprint here for authentication (all to do with login and sign up (user auth))

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from . import db
from . import mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message, Mail



auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
# when the user loggs in ,I want to send them an email saying they have logged in into a new session
def login():
    if request.method == 'POST':
       email = request.form.get('email')
       password = request.form.get('password')
       user = User.query.filter_by(email=email).first()
       if user: 
          if check_password_hash(user.password, password): 
             flash('logged in sucessefully! ', category='success')
             login_user(user, remember=True) # this will create a session for the user and it will be true until 
             # he ends the session, restarts the server ( a session is the time interval between login and logout)
             # so for future requests ,we will know that the user is the same one logged in 
             # this is user-authorization
            # msg = Message('LOGGED IN', sender='mayakhawla2@gmail.com', recipients=['daghada06@gmail.com'])
             # msg.body=f"""you've logged in our notes' app!!
             # infos : email : {email}
             #        password : {generate_password_hash(password)}
            # """
             # mail.send(msg)
             return redirect(url_for('views.home'))
          else: 
             flash('incorrect password, try again!', category='error')
       else: 
          flash('email does not exist! ', category='error')   

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user() # this will log out the current user , means remove user from the session
    return redirect(url_for('auth.login')) # after they log out we will bring them to the login page again

@auth.route('/sign-up',methods=['GET', 'POST'])
# accepting and handling the post request sent by the form
# when we create a function for a route the default method is get , so that function will
#  reply to our user's get reqyest sent via a web browser with whatever the function on our route returns 
# and in most cases it's an html page 
# if we want to send a post request , we should specify it as above  
def signup():
     data = request.form
     email = data.get('email')
     firstname = request.form.get('firstName')
     password1 = request.form.get('password1')
     password2 = request.form.get('password2')
     # when we sign up , we need to make sure the user doesn't already exist 
     user = User.query.filter_by(email=email).first()
     if user: 
         flash('Email already exists!!', category='error')
     else:    
      if  (( email==None) or  ( firstname==None) or ( password1==None) or ( password2==None)):
        flash('the form is missing some fileds, filling all the fields ir required.', category='error')
      elif len(email)< 4: 
        flash('email must be greater than 3 characters! ', category='error')
      elif len(firstname) < 3: 
        flash('first name is too short !!', category='error')
      elif password1!= password2: 
        flash('passwords not matching !!', category='error')
      else:
        new_user = User(email=email, firstName=firstname, password = generate_password_hash(password1, method='sha256'))
        db.session.add(new_user) # this is the session we are removing the user from
        db.session.commit() 
        login_user(user, remember=True)
        flash('account created successfully! ', category='success')
        # now that the user is created secussfully , we will redirect the user to the home page
        return redirect(url_for('views.home'))
        
     return render_template('signup.html',user=current_user)


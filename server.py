from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


#Creating homepage route!

@app.route("/")
def show_homepage():
    """Show homepage"""

    return render_template('homepage.html')

@app.route('/login', methods = ['POST'])
def login():
    """ Login with email and password """

    email = request.form.get('email')
    password = request.form.get('password')

    user_password = crud.get_password_by_email(email)

    if user_password == password:
        session['user'] = crud.get_user_id_by_email(email)
        flash('Logged in!')
    else:
        flash('Incorrect password, please try again!')

    return redirect('/')

@app.route('/new_users', methods = ['POST'])
def register_user():
    """ Create a new user """

    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    dog_name = request.form.get('dog_name')
    dog_age = request.form.get('dog_age')
    dog_size = request.form.get('dog_size')
    dog_breed = request.form.get('dog_breed')
    
    user = crud.get_user_by_email(email)
    

    if user:
        flash('This email has already been used. Try a different email.')
    else:
        new_user = crud.create_user(fullname, email, password, address)
        db.session.add(new_user)
        db.session.commit()
        # user_id = new_user.user_id
        user = crud.get_user_id_by_email(email)
        dog = crud.create_dog_profile(user, dog_name, dog_age, dog_size, dog_breed)
        db.session.add(dog)
        db.session.commit()
        flash('Your account has been successfully created. You can log in now')

    return redirect('/')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def show_homepage():
    """Show homepage"""

    return render_template('homepage.html')

@app.route('/login', methods = ['POST'])
def login():
    """ Login with email and password """

    #Getting data from the form
    email = request.form.get('email')
    password = request.form.get('password')

    #Get user's password to check if the ented password is correct
    user_password = crud.get_password_by_email(email)

    if user_password == password:
        session['user'] = crud.get_user_id_by_email(email)
        flash('Logged in!')
        return redirect('/all_profiles')
    else:
        flash('Incorrect password, please try again!')

        return redirect('/')

@app.route('/new_users', methods = ['POST'])
def register_user():
    """ Create a new user """

    #Getting all the data from the form in homepage.html
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    dog_name = request.form.get('dog_name')
    dog_age = request.form.get('dog_age')
    dog_size = request.form.get('dog_size')
    dog_breed = request.form.get('dog_breed')
    
    #Getting user object to check if they are already registered 
    user = crud.get_user_by_email(email)

    if user:
        flash('This email has already been used. Try a different email.')
    else:
        new_user = crud.create_user(fullname, email, password, address) 
        db.session.add(new_user) #Adding the new user to data base
        db.session.commit()
        user = crud.get_user_id_by_email(email)
        dog = crud.create_dog_profile(user, dog_name, dog_age, dog_size, dog_breed)
        db.session.add(dog) #Adding user's dog to the data base
        db.session.commit()
        flash('Your account has been successfully created. You can log in now')

    return redirect('/')


@app.route('/all_profiles')
def show_all_profiles():
    """ Return dog profiles """

    if "user" in session:
        user_id = session["user"]
    
    user= crud.get_user_by_id(user_id)

    #Get all user objects and display them on the page
    users = crud.show_all_users()

    return render_template('all_profiles.html', users=users, user_id=user_id, user=user)


@app.route('/write_message')
def write_message():
    """Take user to textbox to write a message"""

    #Getting the user_id from the button to send a message, on all_profiles.html
    #And then setting that botton to a receiver_id, and then storing in a session
    receiver_id = request.args.get('user_id')
    session['receiver_id'] = receiver_id

    return render_template("write_message.html", receiver_id=receiver_id)


@app.route('/inbox', methods = ['POST'])
def creating_inbox():
    "Creating inbox"

    if "user" in session:
        user = session["user"]

    if "receiver_id" in session:
        receiver_id = session["receiver_id"]
    
    #Getting all data from the form write_message.html
    body = request.form.get('message')
    date = datetime.now()
    message = crud.create_message(user, receiver_id, body, date)
    db.session.add(message)
    db.session.commit()

    return redirect("/inbox_")


@app.route('/inbox_')
def show_all_messages():
    """ Return all messages from a specific user """

    if "user" in session:
        user_id = session["user"]

    if "receiver_id" in session:
        receiver_id = session["receiver_id"]

    #Getting all the messages sent and received from user
    messages_from_me = crud.get_messages_sent_received(user_id, receiver_id)
    #Getting all the messages sent and received from the receiver user
    messages_to_me = crud.get_messages_sent_received(receiver_id, user_id)

    # Concatenating the two lists above, so we have all the messages from/to user
    messages = messages_from_me + messages_to_me
    #Sorting the concatenated list by time, so it appears in cronologic time
    sorted_messages_by_date = crud.sort_list_by_date(messages)

    return render_template('inbox.html', sorted_messages_by_date=sorted_messages_by_date)

@app.route('/main_inbox')
def main_inbox():
    """ return a list of user's name that exchanged messages """

    if "user" in session:
        user_id = session["user"]

    if "receiver_id" in session:
        receiver_id = session["receiver_id"]

    #Getting all the user messages
    all_user_messages = crud.get_messages_sent_received(user_id, receiver_id)
    #Get all the receiver_id's from all_user_messages list, so there are no duplicate names in the "/main_inbox"
    all_user_messages = crud.all_receiver_id()


    list_of_users_for_inbox =[]
    for message in all_user_messages:
        if message.receiver_id != user_id: #so the user's name is not displayed
            user = crud.get_user_by_id(message.receiver_id)
            list_of_users_for_inbox.append(user) #appending the user's to the list, with no duplicates 

    return render_template('main_inbox.html', list_of_users_for_inbox=list_of_users_for_inbox )



@app.route('/show_inbox')
def show_inbox():
    """Show user names in inbox """

    #This route is really similar to @app.route('/inbox_'). I created this route due the fact that I need to pass
    # a new receveicer_id, coming from a button in the main_inbox html file.

    if "user" in session:
        user_id = session["user"]

    #getting user_id from the button in main_inbox.html
    receiver_id = request.args.get('user_id')

    #Function used yo avoid repetiton, it consists on the content in lines 130 - 137
    sorted_messages_by_date = crud.inbox_function(user_id, receiver_id)


    return render_template('inbox.html', sorted_messages_by_date=sorted_messages_by_date)


@app.route('/profile')
def show_user_profile():
    """ User's profile  page"""

    if "user" in session:
        user_id = session["user"]

    #gettin the user info from user to display on their profile
    user = crud.get_user_by_id(user_id)

    return render_template("profile.html", user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
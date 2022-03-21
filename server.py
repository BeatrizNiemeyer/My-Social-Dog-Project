from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
from model import db, User, Dog, Message, connect_to_db

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
    dog_breed = dog_breed.lower()
   
    
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

    return redirect("/inbox")


@app.route('/inbox')
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


    user = crud.get_user_by_id(user_id)
    
    #gettind ids for the list of names

    list_of_receivers = [users.receiver_id for users in user.messages_sent if user.user_id == users.sender_id]
    # list_of_receivers = []
    # for users in user.messages_sent:
    #     if user.user_id == users.sender_id:
    #         list_of_receivers.append(users.receiver_id)
    
    list_of_senders = [users.sender_id for users in user.messages_received if user.user_id == users.receiver_id]

    # for users in user.messages_received:
    #     if user.user_id == users.receiver_id:
    #         list_of_senders.append(users.sender_id)
 
    list_of_ids = list_of_receivers + list_of_senders
    list_of_ids = set(list_of_ids)

    list_of_users_for_inbox =[]
    for each_id in list_of_ids:
        if each_id != user_id: #so the user's name is not displayed
            user = crud.get_user_by_id(each_id)
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


@app.route("/profile")
def show_user_profile():
    """ User's profile  page"""

    if "user" in session:
        user_id = session["user"]

    #getting the user info from user to display on their profile
    user = crud.get_user_by_id(user_id)

    return render_template("profile.html", user=user)


@app.route("/search")
def search():
    """ Show searching results """

    if "user" in session:
        user_id = session["user"]

    user = crud.get_user_by_id(user_id)
    users = crud.show_all_users()
  
    #getting info from searching bar:
    dog_age = request.args.get("dog_age")
    dog_size = request.args.get("dog_size")
    dog_breed = request.args.get("dog_breed")
    searched_distance = request.args.get("distance")
    dog_age = int(dog_age)
    searched_distance = int(searched_distance)

    #creating a dictionary with the values from the search
    results = {}
    results["dog_age"] = dog_age
    results["dog_size"] = dog_size
    results["dog_breed"] = dog_breed
    results["searched_distance"] = searched_distance

    #getting latitude and longitud from user's address
    user_coordinates = crud.get_coordinates(user.address)
   
    #This list will contain the users with the dogs that "pass" the searching results
    list_of_searched_dogs = []

    #if user press enter without entering any searching feature, it will redirect user to /all_profiles with all the profiles
    if results["dog_size"] == "all_sizes" and results["dog_age"] == 17 and results["dog_breed"] == "" and results["searched_distance"] == 1000000:
        return redirect ("/all_profiles")
    else:    
        for user in users:
            #getting latitude and longitud from every user address
            coordinates = crud.get_coordinates(user.address)
            #calculating the distance between user and the other user
            distance = crud.distance_between_users(user_coordinates, coordinates)
            if distance <= results["searched_distance"]:
                for every_user in user.dogs:
                    if every_user.dog_age <= dog_age and every_user.dog_size == dog_size and every_user.dog_breed == dog_breed:
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif results["dog_age"] == 17 and every_user.dog_size == dog_size and every_user.dog_breed == dog_breed:
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif every_user.dog_age <=dog_age and results["dog_size"] == "all_sizes" and every_user.dog_breed == dog_breed:
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif every_user.dog_age <=dog_age and every_user.dog_size == dog_size and results["dog_breed"] == "":
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif results["dog_age"] == 17 and results["dog_size"] == "all_sizes" and  every_user.dog_breed == dog_breed:
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif results["dog_age"] == 17 and every_user.dog_size == dog_size and results["dog_breed"] == "":
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
                    elif every_user.dog_age <= dog_age and results["dog_size"] == "all_sizes" and results["dog_breed"] == "":
                        user = crud.get_user_by_id(every_user.user_id)
                        list_of_searched_dogs.append(user)
    
    list_of_searched_dogs = set(list_of_searched_dogs)
        
    return render_template('all_profiles.html', users=list_of_searched_dogs, user_id=user_id, user=user)
        
@app.route("/update_user")
def update_user():
    """ User update profile """

    if "user" in session:
        user_id = session["user"]

    fullname = request.args.get('fullname')
    password = request.args.get('password')
    address = request.args.get('address')

    db.session.query(User).filter(User.user_id == user_id).update({"fullname": fullname, "password":password, "address":address})
    db.session.commit()

    user = crud.get_user_by_id(user_id)

    return render_template("/profile.html", user=user)

@app.route("/add_dog")
def add_dog():
    """ Adding a new dog """

    if "user" in session:
        user_id = session["user"]

    dog_name = request.args.get('dog_name')
    dog_age = request.args.get('dog_age')
    dog_size = request.args.get('dog_size')
    dog_breed = request.args.get('dog_breed')
    dog_breed = dog_breed.lower()

    dog = crud.create_dog_profile(user_id, dog_name, dog_age, dog_size, dog_breed)
    db.session.add(dog) #Adding user's dog to the data base
    db.session.commit()
    flash('Your account has been successfully created. You can log in now')

    return redirect("/profile")



@app.route("/delete_account")
def delete_account():
    """ Delete user's account """

    if "user" in session:
        user_id = session["user"]

    user = crud.get_user_by_id(user_id)


    db.session.delete(user)
    db.session.commit()
    flash("Your account was deleted!")

    return redirect ("/")

@app.route("/logout")
def logout_user():
    """ Process of logout """

    del session["user"]
    flash("You are now logout")

    return redirect("/")



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
from model import db, User, Dog, connect_to_db
import os
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


API_KEY = os.environ["MAP_API"]
CLOUDINARY_KEY = os.environ["CLOUDINARY_KEY"]
CLOUDINARY_SECRET = os.environ["CLOUDINARY_SECRET"]
CLOUD_NAME = "dxvo8obxj"


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

    #Get user's password to check if the entered password is correct
    user = crud.get_user_by_email(email)

    if user and password:
        user_password = crud.get_password_by_email(email)
        user = crud.get_user_by_email(email)

        if crud.check_hash_password(password, user_password):
            session['user'] = crud.get_user_id_by_email(email)
            flash('Logged in!')
            return redirect('/all_profiles')
        else:
            flash('Incorrect password, please try again!')
    else:
        flash('Information is incorrect, try again!')

            
    return redirect('/')

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route('/new_users', methods = ['POST'])
def register_user():
    """ Create a new user """

    #Getting all the data from the form in homepage.html
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = crud.hash_password(password)
    address = request.form.get('address')
    dog_name = request.form.get('dog_name')
    dog_age = request.form.get('dog_age')
    dog_size = request.form.get('dog_size')
    dog_breed = request.form.get('dog_breed')
    dog_breed = dog_breed.lower()

    
    #Getting user object to check if they are already registered 
    user = crud.get_user_by_email(email)
    longitude = crud.get_longitude(address)
    latitude = crud.get_latitude(address)

    if user:
        flash('This email has already been used. Try a different email.')
    elif fullname and email and password and address and dog_name and dog_age and dog_size and dog_breed:
        new_user = crud.create_user(fullname, email, hashed_password, address, longitude, latitude) 
        db.session.add(new_user) #Adding the new user to data base
        db.session.commit()
        profile_photo = "/static/images/corgi_emogi.png"
        db.session.query(User).filter(User.email == email).update({"profile_photo":profile_photo})
        db.session.commit()
        user = crud.get_user_id_by_email(email)
        dog = crud.create_dog_profile(user, dog_name, dog_age, dog_size, dog_breed)
        db.session.add(dog) #Adding user's dog to the data base
        db.session.commit()
        flash('Your account has been successfully created. You can log in now')
    elif fullname and email and password and address:
        new_user = crud.create_user(fullname, email, hashed_password, address, longitude, latitude) 
        db.session.add(new_user) #Adding the new user to data base
        db.session.commit()
        flash('Your account has been successfully created. You can log in now')
        profile_photo = "/static/images/corgi_emogi.png"
        db.session.query(User).filter(User.email == email).update({"profile_photo":profile_photo})
        db.session.commit()
    else:
       flash("Missing Information!")

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


    return render_template('inbox.html', sorted_messages_by_date=sorted_messages_by_date, receiver_id=receiver_id)

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


    return render_template('inbox.html', sorted_messages_by_date=sorted_messages_by_date, receiver_id=receiver_id)


@app.route("/profile")
def show_user_profile():
    """ User's profile  page"""

    if "user" in session:
        user_id = session["user"]

    #getting the user info from user to display on their profile
    user = crud.get_user_by_id(user_id)

    return render_template("profile.html", user=user)

@app.route("/upload_picture", methods = ['POST'])
def upload_picture():
    """ Uploads a dog picture and adds it to database """

    if "user" in session:
        user_id = session["user"]

    user= crud.get_user_by_id(user_id)
    users = crud.show_all_users()

    dog_picture = request.files["dog_picture"]
    result = cloudinary.uploader.upload(dog_picture,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name=CLOUD_NAME)
    
    profile_photo = result['secure_url']

    db.session.query(User).filter(User.user_id == user_id).update({"profile_photo":profile_photo})
    db.session.commit()
    flash('Your profile was updated!')

    return redirect("/profile")


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
    dog_breed = dog_breed.lower()
    searched_distance = int(searched_distance)

    #creating a dictionary with the values from the search
    results = {}
    results["dog_age"] = dog_age
    results["dog_size"] = dog_size
    results["dog_breed"] = dog_breed
    results["searched_distance"] = searched_distance

    #getting latitude and longitud from user's address
    user_coordinates = (user.longitude, user.latitude)
   
   #joining user and dog and filtering dogs through the searching results
    dogs = db.session.query(User).join(Dog)
    if dog_age:
        dogs = dogs.filter(Dog.dog_age <= dog_age)
    if dog_size and dog_size != "all_sizes":
        dogs = dogs.filter(Dog.dog_size == dog_size)
    if dog_breed:
        dogs = dogs.filter(Dog.dog_breed == dog_breed)

    #this list contains all the dogs that "passes" search
    dogs_list = dogs.all()
    #making sure users are not repeated
    set_of_searched_dogs = set()
    if results["searched_distance"] <= 1000000:
        for user in dogs_list:
            coordinates = (user.longitude, user.latitude)
            #calculating the distance between user and the other user
            distance = crud.distance_between_users(user_coordinates, coordinates)
            #if distance between users are appropriate, the user will be appended into the set_of_searched_dogs list
            if distance <= results["searched_distance"]:
                set_of_searched_dogs.add(user)

        
    return render_template('all_profiles.html', users=set_of_searched_dogs, user_id=user_id, user=user)
        
@app.route("/update_user")
def update_user():
    """ User update profile """

    if "user" in session:
        user_id = session["user"]

    fullname = request.args.get('fullname')
    address = request.args.get('address')
    if fullname and address:
        longitude = crud.get_longitude(address)
        latitude = crud.get_latitude(address)
        db.session.query(User).filter(User.user_id == user_id).update({"fullname": fullname, "address":address, "longitude":longitude, "latitude":latitude})
        db.session.commit()
        flash('Your profile was updated!')
    elif fullname:
        db.session.query(User).filter(User.user_id == user_id).update({"fullname": fullname})
        db.session.commit()
        flash('Your profile was updated!')
    elif address:
        longitude = crud.get_longitude(address)
        latitude = crud.get_latitude(address)
        db.session.query(User).filter(User.user_id == user_id).update({"address":address, "longitude":longitude, "latitude":latitude})
        db.session.commit()
        flash('Your profile was updated!')
    else:
        flash('Missing data!')


    return redirect("/profile")

@app.route("/add_dog.json", methods=["POST"])
def add_dog():
    """ Adding a new dog """

    if "user" in session:
        user_id = session["user"]

    dogName = request.get_json().get('dogName')
    dogAge = request.get_json().get('dogAge')
    dogSize = request.get_json().get('dogSize')
    dogBreed = request.get_json().get('dogBreed')
    dogBreed = dogBreed.lower()
 


    dog = crud.create_dog_profile(user_id, dogName, dogAge, dogSize, dogBreed)
    db.session.add(dog) #Adding user's dog to the data base
    db.session.commit()

    new_dog = {
        "dogName": dogName,
        "dogAge":dogAge,
        "dogSize": dogSize,
        "dogBreed": dogBreed,
        "dogId": dog.dog_id
    }


    return jsonify({"dogAdded": new_dog})
  
@app.route("/show_user_dogs")
def show_dog():
    """return user dogs"""

    if "user" in session:
        user_id = session["user"]

    dogs = crud.get_user_dog(user_id)

    list_of_dogs = []

    for dog in dogs:
        dog_data = {"dogName": dog.dog_name, "dogAge": dog.dog_age, "dogSize":dog.dog_size, "dogBreed":dog.dog_breed, "dogId": dog.dog_id}
        list_of_dogs.append(dog_data)

    print("**************************************")
    print(list_of_dogs)

    return jsonify({"dogs": list_of_dogs})


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

@app.route("/map")
def see_map():
    """Display map using user's geolocation"""

    return render_template("map.html")


@app.route("/dog_fact")
def dog_fact():
    """ Returns a random dog fact """

    dog_fact = crud.dog_fact()

    return dog_fact

@app.route("/calendar")
def see_calendar():
    """Display calendar"""

    return render_template("calendar.html")

@app.route("/create_event", methods = ['POST'])
def create_event():
    """Create event and storage it in the db """

    if "user" in session:
        user_id = session["user"]

    event_body = request.form.get('event_name') 
    date_for_event = request.form.get('event_date') #string 2022-04-05, i need to convert it like >> 04/05/2022
    event_time_str = request.form.get('event_time') #string in 24hour >> convert to datetime and in 12hour format
    event_time = datetime.strptime(event_time_str, '%H:%M') #time in datetime

    correct_date = date_for_event.split("-")
    year = correct_date[0] 
    month = correct_date[1]
    day = correct_date[2]

    if int(month) < 10:
        month = month[1:2]

    if int(day) < 10:
        day = day[1:2]

    event_date = month + "/" + day + "/" + year

    if int(event_time_str[:2]) < 12:
        time = event_time_str + "AM"
    elif int(event_time_str[:2]) == 12:
        time = event_time_str + "PM"
    else:
        time = str(int(event_time_str[:2]) - 12) + event_time_str[2:] + "PM"

    event = crud.create_event(user_id, event_body, event_date, event_time, time )
    db.session.add(event)
    db.session.commit()
    flash("Your event was created!")

    return redirect('/calendar')


@app.route("/get_event")
def get_user_events():
    """get a list of  user's events"""

    if "user" in session:
        user_id = session["user"]

    #getting user events
    events = crud.get_event_by_id(user_id)

    #sorting events by time
    sorted_events = crud.sort_list_by_time(events)
    
    list_events = []

    #creating a dictionary with event info and appending to a list
    for event in sorted_events:
        event_dict = {"id": str(event.event_id), "date": event.event_date_str, "body":event.event_body, "time": event.event_time_str}
        list_events.append(event_dict)

    return jsonify(list_events)


@app.route("/delete_event")
def delete_event():
    """delete an event"""

    #getting event_id from form
    event_id = request.args.get("event_id")
   
   #getting event object
    event = crud.get_event(event_id)
  
    #deleting it
    db.session.delete(event)
    db.session.commit()
    flash("Your event was deleted!")

    return redirect ("/calendar")


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
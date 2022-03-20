from model import db, User, Dog, Message, connect_to_db
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="geopy.geocoders.options.default_user_agent = 'my-application'")

def create_user(fullname, email, password, address):
    """Create and return a new user."""

    user = User(fullname=fullname, email=email, password=password, address=address)

    return user

def get_password_by_email(email):
    """ Return a password by user email """

    user = User.query.filter(User.email==email).first()
    
    return user.password

def get_user_id_by_email(email):
    """ Return user id by user email"""

    user = User.query.filter(User.email==email).first()

    return user.user_id


def get_user_by_email(email):
    """Return a user by their email """

    user = User.query.filter(User.email==email).first()

    return user

def get_user_by_id(user_id):
    """Return a user by their email """

    user = User.query.get(user_id)

    return user


def create_dog_profile(user_id, dog_name, dog_age, dog_size, dog_breed):
    """ Create and return a dog profile """

    dog = Dog(user_id=user_id, dog_name=dog_name, dog_age=dog_age, dog_size=dog_size, dog_breed=dog_breed)

    return dog


def show_all_users():
    """ Return all users """

    users = User.query.all()

    return users

def show_all_dogs():
    """Return all dogs """

    dogs = Dog.query.all()

    return dogs


def create_message(sender_id, receiver_id, body, date):
    """Create a message """

    message = Message(sender_id=sender_id, receiver_id=receiver_id, message_body=body, message_date=date)

    return message



def get_all_users():
    """Return all users """

    all_users = User.query.all()

    return all_users


def get_messages_sent_received(sender_id, receiver_id):
    """get all the messages the user received and sent """

    messages = Message.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()

    return messages

def user_all_messages(user_id):
    """ get user's all messages """

    all_messages = Message.query.filter_by(user_id=user_id)

    return all_messages 
    
def sort_list_by_date(list_of_messages):
    """ sort messages by date """

    sorted_messages = sorted(list_of_messages, key=lambda every_item: every_item.message_date)

    return sorted_messages

def all_receiver_id():

    """ Group by receiver_id """

    q = db.session.query(Message.receiver_id)
    all_receiver_id = q.group_by("receiver_id")

    return all_receiver_id

def inbox_function(user_id, receiver_id):
    """ function used on lines 130 - 137, so there is less repetition """

    #Getting all the messages sent and received from user
    messages_from_me = get_messages_sent_received(user_id, receiver_id)
    #Getting all the messages sent and received from the receiver user
    messages_to_me = get_messages_sent_received(receiver_id, user_id)

    # Concatenating the two lists above, so we have all the messages from/to user
    messages = messages_from_me + messages_to_me
    #Sorting the concatenated list by time, so it appears in cronologic time
    sorted_messages_by_date = sort_list_by_date(messages)

    return sorted_messages_by_date


def get_coordinates(address):
    """ Get coordinates to calculate distance """


    user_location = geolocator.geocode(address)
    user_coordinates = (user_location.latitude, user_location.longitude)

    return user_coordinates

def distance_between_users(coordinate1, coordinate2):
    """ Calculate distance between users """

    distance = (geodesic(coordinate1,coordinate2).km)
    distance_miles = distance * 0.625

    return distance_miles

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

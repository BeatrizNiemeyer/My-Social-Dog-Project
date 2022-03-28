from model import db, User, Dog, Message, connect_to_db
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random
import hashlib


geolocator = Nominatim(user_agent="geopy.geocoders.options.default_user_agent = 'my-application'")

def create_user(fullname, email, password, address, longitude, latitude):
    """Create and return a new user."""

    user = User(fullname=fullname, email=email, password=password, address=address, longitude=longitude, latitude=latitude)

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


def get_latitude(address):
    """ Get coordinates to calculate distance """


    user_location = geolocator.geocode(address)
    user_latitude = user_location.latitude
  
    return user_latitude

def get_longitude(address):
    """ Get coordinates to calculate distance """


    user_location = geolocator.geocode(address)
    user_longitude = user_location.longitude

    return user_longitude

def distance_between_users(coordinate1, coordinate2):
    """ Calculate distance between users """

    distance = (geodesic(coordinate1,coordinate2).km)
    distance_miles = distance * 0.625

    return distance_miles


def dog_fact():
    """Retuns a random dog fact """

    dog_facts =[ 
        "Did you know that... A dog's nose print is unique, much like a person's fingerprint!",
        "Did you know that... Forty-five percent of U.S. dogs sleep in their owner's bed!",
        "Did you know that... All dogs dream, but puppies and senior dogs dream more frequently than adult dogs!",
        "Did you know that... Seventy percent of people sign their dog's name on their holiday cards!",
        "Did you know that... Dogs have a great sense of smell! Their nose have as many as 300 million receptors. In comparison, a human nose has about 5 million!",
        "Did you know that... Dogs' noses can sense heat/thermal radiation, which explains why blind or deaf dogs can still hunt!",
        "Did you know that... Dogs curl up in a ball when sleeping to protect their organs—a hold over from their days in the wild, when they were vulnerable to predator attacks!",
        "Did you know that... Yawning is contagious—even for dogs. Research shows that the sound of a human yawn can trigger one from your dog!",
        "Did you know that... Human blood pressure goes down when petting a dog. And so does the dog's!",
        "Did you know that... Dogs are not colorblind. They can see blue and yellow!",
        "Did you know that... The Australian Shepherd is not actually from Australia—they are an American breed!",
        "Did you know that... All puppies are born deaf!",
        "Did you know that... Dalmatians are born completely white, and develop their spots as they get older!",
        "Did you know that... Dogs have about 1,700 taste buds. We humans have between 2,000 - 10,000!",
        "Did you know that... When dogs kick backward after they go to the bathroom it's not to cover it up, but to mark their territory, using the scent glands in their feet!",
        "Did you know that... A recent study shows that dogs are among a small group of animals who show voluntary unselfish kindness towards others without any reward!",
        "Did you know that... Your dog could be left or right-pawed!",
        "Did you know that... Dogs have 18 muscles controlling their ears!",
        "Did you know that... Dogs are about as intelligent as a two-year-old!",
        "Did you know that... Dogs noses are wet to help absorb scent chemicals!",
        "Did you know that... Three dogs survived the Titanic sinking!",
        "Did you know that... A Greyhound could beat a Cheetah in a long distance race!",
        "Did you know that... Dog socialization reduces fear and anxiety!",
        "Did you know that... Dog socialization improves intelligence and behavior!",
    ]

    return random.choice(dog_facts)

def hash_password(password):
    """ Converts password to hash """

    return hashlib.sha256(str.encode(password)).hexdigest()

    
def check_hash_password(password, hash):
    """Checks if password input matches hashed password """

    if hash_password(password) == hash:
        return True
        
    return False

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

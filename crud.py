from model import db, User, Dog, Message, connect_to_db

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


def get_messages_sent(user_id):

    """Return all messages"""

    messages = Message.query.filter(Message.sender_id==user_id).all()

    return messages

def get_messages_received(receiver_id):

    """Return all messages"""

    messages = Message.query.filter(Message.receiver_id==receiver_id).all()

    return messages

def get_all_messages_by_users(fullname):
    """ return all messages from a person """

    person = Message.query.filter(Message.fullname==fullname).all()

    return person.message_body



if __name__ == '__main__':
    from server import app
    connect_to_db(app)

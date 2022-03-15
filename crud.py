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

def create_dog_profile(user_id, dog_name, dog_age, dog_size, dog_breed):
    """ Create and return a dog profile """

    dog = Dog(user_id=user_id, dog_name=dog_name, dog_age=dog_age, dog_size=dog_size, dog_breed=dog_breed)

    return dog

















if __name__ == '__main__':
    from server import app
    connect_to_db(app)

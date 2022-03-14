from model import db, User, Dog, Message, connect_to_db

def create_user(fullname, email, password, address):
    """Create and return a new user."""

    user = User(fullname=fullname, email=email, password=password, address=address)

    return user


def create_dog_profile(dog_name, dog_age, dog_size, dog_breed):
    """ Create and return a dog profile """

    dog = Dog(dog_name=dog_name, dog_age=dog_age, dog_size=dog_size, dog_breed=dog_breed)

    return dog

















if __name__ == '__main__':
    from server import app
    connect_to_db(app)

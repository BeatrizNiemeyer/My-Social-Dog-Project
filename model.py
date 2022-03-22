""" Models for my-social-dog project. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ User information """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password= db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    dogs = db.relationship("Dog", back_populates="user")
    #messages_sent = db.relationship("Message", backref="sender")
    #messages_received = db.relationship("Message", backref="receiver")

    # def __repr__(self):
    #     return f"<User user_id={self.user_id} email={self.email}>"


class Dog(db.Model):
    """ Dog information """

    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey("users.user_id"))
    dog_name = db.Column(db.String, nullable=False)
    dog_age = db.Column(db.Integer, nullable=False)
    dog_size = db.Column(db.String, nullable=False)
    dog_breed = db.Column(db.String, nullable=True)
    dog_photo = db.Column(db.String, nullable=True)

    user = db.relationship("User", back_populates="dogs")

    # def __repr__(self):
    #     return f"<Dog dog_id={self.dog_id} dog_name={self.dog_name} dog_user={self.user_id}>"


class Message(db.Model):
    """ Message information """

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    message_body = db.Column(db.String, nullable=False)
    message_date = db.Column(db.DateTime) 

    sender = db.relationship("User", backref="messages_sent", foreign_keys="Message.sender_id")
    receiver = db.relationship("User", backref="messages_received", foreign_keys="Message.receiver_id")

    # def __repr__(self):
    #     return f"<Message message_id={self.message_id} sender_id={self.sender_id} receiver_id={self.receiver_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///msd_data", echo=True):
    """Conecting to db"""
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


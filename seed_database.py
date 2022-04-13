"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
from model import db, User, Dog, Message, Event, connect_to_db
import server

os.system("dropdb msd_data")
os.system("createdb msd_data")

connect_to_db(server.app)
db.create_all()

with open('data/users.json') as f:
    user_data = json.loads(f.read())


users_in_db = []
for user in user_data:
    fullname = user['fullname']
    email = user['email']
    password = user['password']
    hashed_password = crud.hash_password(password)
    address = user['address']
    longitude = crud.get_longitude(address)
    latitude = crud.get_latitude(address)

    dog_name = user['dog_name']
    dog_age = user['dog_age']
    dog_size = user['dog_size']
    dog_breed = user['dog_breed']
    dog_breed = dog_breed.lower()
    
    new_user = crud.create_user(fullname, email, hashed_password, address, longitude, latitude) 
    db.session.add(new_user)
    db.session.commit()

    profile_photo = "/static/images/corgi_emogi.png"
    db.session.query(User).filter(User.email == email).update({"profile_photo":profile_photo})
    db.session.commit()

    user_id = crud.get_user_id_by_email(email)
    dog = crud.create_dog_profile(user_id, dog_name, dog_age, dog_size, dog_breed)
    db.session.add(dog) 
    db.session.commit()



import unittest

from server import app
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, example_data, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
from model import db, User, Dog, Message, connect_to_db
import os
import cloudinary.uploader


class MySocialDogTests(unittest.TestCase):
    """Tests for MySocialDog app """

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] =  True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Log In", result.data)

    def test_calendar(self):
        result = self.client.get("/calendar")
        self.assertIn(b"Create an Event!", result.data)
        

class MySocialDogDataBase(unittest.TestCase):
    """Tests for MySocialDog database"""

    def setUp(self):
        """ To do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///msd_data")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """ Test the sign up form"""
        result = self.client.post("/login", data={'fullname': 'Ray', 'email': 'raymond@hb.com', 'password': '123', 'address': '7 N 8th St, Richmond VA', 'profile_photo': 'https://images.emojiterra.com/google/android-11/512px/1f436.png', 'longitude': '-77.51126620527393', 'latitude':'37.639684450000004'},
                                            follow_redirects=True)
        self.assertIn(b"Log In", result.data)



if __name__ == "__main__":
    unittest.main()
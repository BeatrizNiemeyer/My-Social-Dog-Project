# My Social Dog
> An app that aims to facilitate dog socialization

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [About the Developer](#about-the-developer)



## General Information
- This app is intended to help users to contact other dog owners that are also interested on socializing their dogs.
-  Dog socialization can benefit dogs in many ways such as reducing stress, anxiety, it helps behavior improvement, and more!
- A registered user will have accesss to other users profiles, where they can read information about their dogs.
- If a user finds a good match for their dog, they can message each other and plan a playdate if both are interested.


## Technologies Used
- Python
- Javascript
- Flask
- Ajax
- Jinja
- Postgresql
- Sqlalchemy
- Google Maps API (Maps JavaScript API, Geolocation API, Places API)
- Cloudinary API



## Features
- Login and registration page.

![login](https://user-images.githubusercontent.com/98921140/164085834-f29485c6-e518-4c16-8a7d-edcd37e91997.gif)


- In the main page, dog profiles are displayed. Users can also search dogs by distance, age, size and breed and message their owners to start a conversation.

![main6](https://user-images.githubusercontent.com/98921140/164104287-ddb09131-bf02-4c71-b27b-28f36daf95b1.gif)

- In the Inbox page, the user can also have access to previous conversations.


![inbox](https://user-images.githubusercontent.com/98921140/164086760-1d451861-89ba-4a5b-b184-ddf0cab84558.gif)


- On My Profile page, users are allowed to upload a dog picture, add a new dog and delete their account.

![profile3](https://user-images.githubusercontent.com/98921140/164104812-9e5cee66-f38a-4e87-bbae-357f9d60734d.gif)


- In the Parks page, parks are shown around the user location. An autocomplete feature enables user to search for establishments nearby.

![maps](https://user-images.githubusercontent.com/98921140/164087117-97701e5a-ca98-4a2f-bf32-5842b0a7ab3d.gif)


- In the Event page, users can add, delete and see their events.

![calendar3](https://user-images.githubusercontent.com/98921140/164103027-fa5d51ec-38d2-4cdf-a6e3-9778537558e4.gif)


## Setup
To run this project:<br>
- You will need to get a google maps API key (enabling Maps JavaScript API, Geolocation API, Places API). Replace your API key in maps.html, on line 50:
"https://maps.googleapis.com/maps/api/js?key=YOUR-API-KEY&libraries=places&callback=initMap"

- You will also need a Cloudinary API key, and store it in secrets.sh

To install it locally:

$ git clone https://github.com/BeatrizNiemeyer/My-Social-Dog-Project.git <br>
$ cd my-social-dog <br>
$ virtualenv env <br>
$ source env/bin/activate <br>
$ pip3 install -r requirements.txt <br>
$ python3 source secrets.sh <br>
$ python3 seed_database.py <br>
$ python3 server.py <br>



## Room for Improvement
- Implement React on calendar
- Make the app responsive 



## Acknowledgements
- Many thanks to my adviser Steve Chait and my mentor Tim Pile for helping me build this project!
- Pictures credits: Alvan Nee and Fatty Corgi


## About the Developer
MySocialDog was created by Beatriz Niemeyer and this is her first project. Learn more about her on [LinkedIn](https://www.linkedin.com/in/beatriz-niemeyer/)


// import axios from 'axios';

function initMap() {
    const location = {
        lat: 37.601773,
        lng: -122.20287,
    };

    const options = {
        center: location,
        zoom: 3,

    }

    //Getting user's location
    if(navigator.geolocation) {
        console.log('geolocation is here!');

        navigator.geolocation.getCurrentPosition((loc) => {
            //if successfull, get the user coordinates
            location.lat = loc.coords.latitude;
            location.lng = loc.coords.longitude;
            // redirect user to basicMap
            const options = {
                center: location,
                zoom: 14,
            }

            //basicMap now has the user coordinates!
            const basicMap = new google.maps.Map(document.querySelector('#map'), (options)); 
            const userLocation = new google.maps.Marker({
            position: location,
            title: 'Your location',
            map: basicMap,
            });

            
            //Request will storage the user location, the radius of the search and the type of search! 
            const request = {
                location: location,
                radius: '500',
                type: ['park']
              };
            
            //console.log(location)
            //Using PlacesService you are able to do nearbySearch and get the places type around your location
            const service = new google.maps.places.PlacesService(basicMap);
            //nearbySearch takes the request data and a callback function (results, status)
            service.nearbySearch(request, (results, status)  => {
           
            //console.log(results)
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                for (let i = 0; i < results.length; i++) {
                createMarker(results[i]);
                }
            }
            
            //creating marker for every result
            function createMarker(place) {
                if (!place.geometry || !place.geometry.location) return;
                const marker = new google.maps.Marker({
                    map: basicMap,
                    position: place.geometry.location,
                    title : place.name,
                });
                }
            },
        )},
            
        //if user doesn't allow the location access, return basicMap
        (err) => {
            console.log('user clicked no');
            // redirect user to basicMap with zoom 2
            const basicMap = new google.maps.Map(document.querySelector('#map'), options); 
        });
    };
}
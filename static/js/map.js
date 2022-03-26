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
                zoom: 15,
            }

            //basicMap now has the user coordinates!
            const basicMap = new google.maps.Map(document.querySelector('#map'), (options)); 
            const userLocation = new google.maps.Marker({
            position: location,
            title: 'Your location',
            map: basicMap,
            icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            });

            //Autocomplete search
            autocomplete = new google.maps.places.Autocomplete(document.querySelector('#search'), {
                componentRestrictions: {'country': ['us']},
                fields: ['geometry', 'name', 'vicinity'],
                types: ['establishment']
            });
        
            autocomplete.addListener('place_changed', () =>{
                const establishment = autocomplete.getPlace();
                basicMap.setCenter(establishment.geometry.location)
                const establishmentMarker= new google.maps.Marker({
                    position: establishment.geometry.location,
                    title: establishment.name,
                    map: basicMap,
                    icon: 'http://maps.google.com/mapfiles/ms/icons/pink-dot.png',
                });
                

                const establishmentInfoWindow = `
                <h6>${establishment.name}</h6>
                <p>
                    Located at: ${establishment.vicinity}
                </p>`;

                const establishmentInfo = new google.maps.InfoWindow({
                    content: establishmentInfoWindow,
                    maxWidth: 200,
                });

                establishmentMarker.addListener('click', () => {
                //Setting a timer of 3 sec to close the window!
                setTimeout(() => {
                    establishmentInfo.close();
                }, 3000),

                establishmentInfo.open(basicMap, establishmentMarker);
                });

            });

            //Request will storage the user location, the radius of the search and the type of search! 
            const request = {
                location: location,
                radius: '5',
                type: ['park']
              };
            
            //console.log(location)
            //Using PlacesService you are able to do nearbySearch and get the places type around your location
            const service = new google.maps.places.PlacesService(basicMap);
            //nearbySearch takes the request data and a callback function (results, status)
            service.nearbySearch(request, (results, status)  => {
           
            console.log(results)
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
                    icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                });

                const parkInfoWindow = `
                <h6>${place.name}</h6>
                <p>
                  Located at: ${place.vicinity}
                </p>`
                ;

                const parkInfo = new google.maps.InfoWindow({
                    content: parkInfoWindow,
                    maxWidth: 200,
                 });

                marker.addListener('click', () => {
                    //Setting a timer of 3 sec to close the window!
                    setTimeout(() => {
                        parkInfo.close();
                    }, 3000),

                    parkInfo.open(basicMap, marker);
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


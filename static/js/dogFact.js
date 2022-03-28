// function dogFact() {
    
//     fetch('/dog_fact')
//     .then(response => response.text())
//     .then(responseData => {
//     document.querySelector('#dog-fact').innerHTML = responseData;
//     });
// }

// document.querySelector('#get-dog-fact').addEventListener('click', dogFact);

// function displayDogFact(){
//     window.setInterval(function(){
//         dogFact()
//     },10000)
  

//Ajax feature to display 'dog fact' every 10 sec!
setInterval(function () {
    
        fetch('/dog_fact')
        .then(response => response.text())
        .then(responseData => {
        document.querySelector('#dog-fact').innerHTML = responseData;
        });
    }, 10000);


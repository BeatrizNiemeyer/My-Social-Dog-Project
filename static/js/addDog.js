document.querySelector('#add-dog-form').addEventListener('submit', (evt) => {
    evt.preventDefault();
  

    const dog_name = document.querySelector('#dog-name').value;
    const dog_age = document.querySelector('#dog-age').value;
    const dog_size = document.querySelector('#dog-size').value;
    const dog_breed = document.querySelector('#dog-breed').value;
    
    const url = `/add_dog.json?dog_name=${dog_name}&dog_age=${dog_age}&dog_size=${dog_size}&dog_breed=${dog_breed}`
  
    fetch(url)
      .then(response => response.json())
      .then(responseJson => {
        document.querySelector('#added-dog').insertAdjacentHTML("beforeend", `<li> Name: ${responseJson.dog_name}</li>`);
        document.querySelector('#added-dog').insertAdjacentHTML("beforeend", ` <li>Age: ${responseJson.dog_age}</li>`);
        document.querySelector('#added-dog').insertAdjacentHTML("beforeend", ` <li>Size: ${responseJson.dog_size}</li>`);
        document.querySelector('#added-dog').insertAdjacentHTML("beforeend", ` <li>Breed: ${responseJson.dog_breed}</li>`);

});
})

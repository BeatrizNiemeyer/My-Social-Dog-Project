function DogInfo(props) {
    return  (
        <ul>
            <li> Name: {props.dogName}</li>
            <li> Age: {props.dogAge} years</li>
            <li> Size: {props.dogSize}</li>
            <li> Breed: {props.dogBreed}</li>
        </ul>
    );
}

function AddDog(props) {
    const [dogName, setName] = React.useState('');
    const [dogAge, setAge] = React.useState('0');
    const [dogSize, setSize] = React.useState('small');
    const [dogBreed, setBreed] = React.useState('');

    function addNewDog() {
      fetch('/add_dog.json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({dogName, dogAge, dogSize, dogBreed}),
        }).then(response => {
        response.json().then(jsonResponse => {
            const {dogAdded} = jsonResponse; // same as dogAdded = jsonResponse.dogAdded
            const {dogName: dogName, dogAge: dogAge, dogSize: dogSize, dogBreed:dogBreed, dogId:dogId} = dogAdded;
            props.addDog(dogName, dogAge, dogSize, dogBreed, dogId);
        });
      });
    }

    return (
      <React.Fragment>
          <h4>Add new dog</h4>
            <p>
            Dog name 
            <input 
                id="dogName" 
                type="text" 
                name="dogName" 
                value={dogName}
                onChange={(event) => setName(event.target.value)}
            ></input>
            </p>

            Dog Age (In years)
             <select 
                id="dogAge" 
                name="dogAge" 
                value={dogAge}
                onChange={(event) => setAge(event.target.value)}>

                <option value= "0"> Less than 1</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>
                <option value="13">13</option>
                <option value="14">14</option>
                <option value="15">15</option>
                <option value="16">More than 15</option>
                
            </select>
            <br></br>

            Dog Size 
            <select 
                id="dogSize" 
                name="dogSize" 
                value={dogSize}
                onChange={(event) => setSize(event.target.value)}>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>

            </select>

            <br></br>
            Dog Breed 
            <input 
                id="dogBreed" 
                type="text" 
                name="dogBreed" 
                value={dogBreed}
                onChange={(event) => setBreed(event.target.value)}>
            </input>
            

            <button type="button" onClick={addNewDog}>Add Dog</button>
      
      </React.Fragment>
    );
  }

  function DogContainer() {
    const [dogs, setDogs] = React.useState([]);
  
    function addDog(dogName, dogAge, dogSize, dogBreed, dogId) {
      const newDog= {dogName:dogName, dogAge:dogAge, dogSize:dogSize, dogBreed:dogBreed, dogId:dogId}; 
      const currentDogs = [...dogs]; 
      setDogs([...currentDogs, newDog]);
    }
  
    React.useEffect(() => {
      fetch('/show_user_dogs')
        .then(response => response.json())
        .then(data => setDogs(data.dogs));
    }, []);
  
    const listOfDogs = [];
  
    for (const currentDog of dogs) {
        console.log(currentDog.dogId)
        listOfDogs.push(
        <DogInfo
          key={currentDog.dogId}
          dogName={currentDog.dogName}
          dogAge={currentDog.dogAge}
          dogSize={currentDog.dogSize}
          dogBreed={currentDog.dogBreed}
        />
      );
    }
  
    return (
      <React.Fragment>
        <AddDog addDog={addDog} />
        <h4>Your Dog information</h4>
        <div >{listOfDogs}</div>
      </React.Fragment>
    );
  }
  
  ReactDOM.render(<DogContainer/>, document.getElementById('dog-container'));
  
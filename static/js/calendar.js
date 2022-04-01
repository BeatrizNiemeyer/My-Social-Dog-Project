function gettingEventData(dayString, daySquare) {
    fetch("/get_event")
        .then(response => response.json())
        .then(responseJSON =>{
            console.log(responseJSON)
            for (const [key, value] of Object.entries(responseJSON)) {
                console.log(responseJSON[key][0]);
                console.log(dayString);

                if (responseJSON[key][0] === dayString){
                    daySquare.classList.add('eventDay');
                    
                }
            // console.log(responseJSON[key][0]) //if date is equal to that
            // console.log(responseJSON[key][1]) // this is the event
            // console.log(responseJSON[key][2]) // this is date and tim
        }})

}

function gettingTodayData(dayString) {
    fetch("/get_event")
        .then(response => response.json())
        .then(responseJSON =>{
            console.log(responseJSON)
            for (const [key, value] of Object.entries(responseJSON)) {
                if (responseJSON[key][0] === dayString){
                    document.querySelector('#eventDay').innerHTML = `<di> Date: ${dayString}</div>`
                    document.querySelector('#show-events').insertAdjacentHTML('beforeend', `<br><div> Event: ${responseJSON[key][1]}</div>
                                                                                          <div> Time: ${responseJSON[key][2]}</div>` )
                };
            }; 
        })
        };


let nav = 0; //each month we are looking at, if is 0, it means today's month!
const calendar = document.querySelector('#calendar'); //selecting div calendar
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']; 

function load() {
    const dt = new Date(); //current date!!
    console.log(dt)
    
    if (nav !== 0) {
        dt.setMonth(new Date().getMonth() + nav, 1); // 01/nav/year
        console.log(dt) //to render the write month, get the current month plus nav to see which month to display
    }

    const day = dt.getDate(); //numeric representation of today's day
    const month = dt.getMonth(); //numeric representation of today's month. january is 0, so march is 2
    const year = dt.getFullYear(); //numeric representation of today's year,

    const firstDayOfMonth = new Date(year, month, 1) // it will print the first day of that nav month. In today's case - Tue Mar 01 2022
    const daysInMonth = new Date(year, month + 1, 0).getDate(); 
    //0 is the last day of previous month
    // month + 1 is the next month
    //getDate returns de day date of that date.

    const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
        weekday: 'long',
        year: 'numeric',
        month: 'numeric',
        day: 'numeric', 
    }); //converts to weekday month/day/year of the first day of the month
    console.log(dateString)

    const paddingDays = weekdays.indexOf(dateString.split(', ')[0]); //if the first day of the month is on a Friday, padding days is 5!  
    //get id element to display month (The whole word, not abv) and year in the top of calendar
    document.querySelector('#monthDisplay').innerText =  `${dt.toLocaleDateString('en-us', { month: 'long' })} ${year}`;
    ;

    calendar.innerHTML = ''; //here we are cleaning our days buttons so we dont create two calendars when clicking next our previous month

    for (let i=1; i <= paddingDays + daysInMonth; i++) {
        const daySquare = document.createElement('div');
        daySquare.classList.add('day');

        const dayString = `${month + 1}/${i - paddingDays}/${year}`


        if (i > paddingDays) {
            daySquare.innerText = i - paddingDays;
            gettingEventData(dayString, daySquare)

            daySquare.addEventListener('click', ()=> {
                document.querySelector('#show-events').innerHTML = ""
                document.querySelector('#eventDay').innerHTML = ""
                fetch("/get_event")
                    .then(response => response.json())
                    .then(responseJSON =>{
                        for (const [key, value] of Object.entries(responseJSON)) {

                            if (responseJSON[key][0] === dayString){
                                document.querySelector('#eventDay').innerHTML = `<di> Date: ${dayString}</div>`
                                document.querySelector('#show-events').insertAdjacentHTML('beforeend', `<br><div> Event: ${responseJSON[key][1]}</div>
                                                                                                        <div> Time: ${responseJSON[key][2]}</div>` )
                            };
                    }});
            
            })

        } else {
            daySquare.classList.add('padding');
        }

        if (i - paddingDays === day && nav === 0){
            daySquare.id = 'currentDay';
            gettingTodayData(dayString); 
          
            
        }
    
    calendar.appendChild(daySquare);
    }
}

function initButtons(){
    document.querySelector('#nextButton').addEventListener('click', () => {
        nav+=1; //incrementing nav (next month)
        document.querySelector('#show-events').innerHTML = ""
        document.querySelector('#eventDay').innerHTML = ""
        load(); //load our calendar
    });
    document.querySelector('#backButton').addEventListener('click', () => {
        nav-=1; //decreasing nav (previous month)
        document.querySelector('#show-events').innerHTML = ""
        document.querySelector('#eventDay').innerHTML = ""
        load(); //load our calendar
    });
}

initButtons();
load();
gettingEventData();

document.querySelector('#registration').addEventListener('click', () => {
    document.querySelector('#registration-form').classList.toggle('hidden');
})

document.querySelector('#dog-registration-button').addEventListener('click', (evt) => {
    evt.preventDefault();
    document.querySelector('#submit-button').classList.toggle('hidden');
    document.querySelector('#dog-registration-form').classList.toggle('dog-form-hidden');
})



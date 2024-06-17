document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript is loaded!");

    const registerForm = document.getElementById('register-form');
    const registerMessage = document.getElementById('register-message');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            email: formData.get('email'),
            phone_number: formData.get('phone_number')
        };

        fetch('http://127.0.0.1:8001/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            registerMessage.innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            registerMessage.innerText = 'Failed to register user.';
        });
    });
});

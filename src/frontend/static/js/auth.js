// Handle sign-in form submission
document.getElementById('signInForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        try {
            const response = await fetch('/user/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();

            if (data.message === "success") {
                document.getElementById('overlay').style.display = 'none';
                window.location.reload();
            } else {
                alert(data.message || 'Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
            alert('Error communicating with the server');
        }
    } else {
        alert("Please enter both username and password.");
    }
});

// Handle registration button click
document.getElementById('registerButton')?.addEventListener('click', async () => {
    const username = document.getElementById('username')?.value;
    const password = document.getElementById('password')?.value;

    if (username && password) {
        try {
            const response = await fetch('/user/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            alert(data.message || 'Registration complete');
        } catch (error) {
            console.error('Error during registration:', error);
            alert('Error communicating with the server');
        }
    } else {
        alert("Please enter both a username and password to register.");
    }
});

// Handle logout functionality
document.getElementById('logoutButton')?.addEventListener('click', async () => {
    try {
        const response = await fetch('/logout', { method: 'POST' });
        const data = await response.json();
        alert(data.message);
        window.location.reload();
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Failed to log out. Please try again.');
    }
});

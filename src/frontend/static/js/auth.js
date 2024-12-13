// Handle sign-in form submission
document.getElementById('signInForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

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
        } catch {
            alert('Error communicating with the server');
        }
    } else {
        alert("Please enter both username and password.");
    }
});

// Handle registration button click
document.getElementById('registerButton')?.addEventListener('click', async () => {
    const username = document.getElementById('username')?.value.trim();
    const password = document.getElementById('password')?.value.trim();

    if (username && password) {
        try {
            const response = await fetch('/user/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            alert(data.message || 'Registration complete');
        } catch {
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
    } catch {
        alert('Failed to log out. Please try again.');
    }
});

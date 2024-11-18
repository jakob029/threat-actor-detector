// Dark mode toggle functionality
document.getElementById('darkModeToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
});

// Check if dark mode was enabled previously
document.addEventListener('DOMContentLoaded', () => {
    const darkModePreference = localStorage.getItem('darkMode') === 'true';
    if (darkModePreference) {
        document.body.classList.add('dark-mode');
    }

    // Check if the overlay is already hidden (handled by Flask template logic)
    const overlay = document.getElementById('overlay');
    if (overlay.style.display === 'none') {
        console.log("User is already signed in. Overlay will remain hidden.");
        return; // Do nothing if already hidden
    }

    // If overlay is visible, assume the user is not signed in
    console.log("User is not signed in. Showing sign-in overlay.");
    overlay.style.display = 'flex';
});

const responseContainer = document.getElementById('responseContainer');
const loader = document.getElementById('loader');
const responseText = document.getElementById('responseText');
const textInputForm = document.getElementById('textInputForm');
const promptInput = document.getElementById('promptInput');

// Handle sign-in form submission
document.getElementById('signInForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        try {
            const response = await fetch('/user/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            console.log("Login response:", data); // Debug log

            if (data.message === "success") {
                document.getElementById('overlay').style.display = 'none';
                console.log("User signed in with UID:", data.uid);

                // Reload the page to update session-based UI
                window.location.reload(); // Alternatively, use window.location.href = '/' if reload fails
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
document.getElementById('registerButton').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        try {
            const response = await fetch('/user/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
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

// Submit the form when "Enter" is pressed in the textarea, but allow "Shift+Enter" for new lines
promptInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        textInputForm.requestSubmit();
    }
});

// Function to handle the prompt submission
async function handlePromptSubmission(event) {
    event.preventDefault();
    const promptText = promptInput.value;
    
    if (promptText) {
        promptInput.value = '';
        responseContainer.classList.add('visible');
        loader.style.display = 'block';
        responseText.innerHTML = '';

        try {
            const formData = new FormData();
            formData.append('prompt', promptText);

            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            loader.style.display = 'none';
            responseText.innerHTML = `<p>Response: ${data.response.replace(/\n/g, '<br>')}</p>`;
        } catch (error) {
            console.error('Error:', error);
            loader.style.display = 'none';
            responseText.innerHTML = '<p>Error fetching response.</p>';
        }
    }
}

// Attach the event listener to the form with async handler
textInputForm.addEventListener('submit', handlePromptSubmission);

// Cookie consent logic
document.addEventListener('DOMContentLoaded', () => {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');
    const infoButton = document.getElementById('infoButton');
    const infoPopup = document.getElementById('infoPopup');
    const closePopup = document.getElementById('closePopup');

    // Ensure cookie consent box is shown only if not already accepted
    if (cookieConsent && cookieConsent.style.display !== 'none') {
        console.log("Showing cookie consent box.");
    } else {
        console.log("Cookies already accepted. Hiding consent box.");
        cookieConsent.classList.add('hidden'); // Ensure it's hidden if already accepted
    }

    // Hide the cookie consent box when "Accept" is clicked and inform the server
    acceptCookies.addEventListener('click', async () => {
        try {
            const response = await fetch('/accept-cookies', { method: 'POST' });
            const data = await response.json();
            console.log(data.message); // Debug log
            cookieConsent.classList.add('hidden'); // Hide the consent box
        } catch (error) {
            console.error('Error accepting cookies:', error);
        }
    });

    // Show the info pop-up when "Info" is clicked
    infoButton.addEventListener('click', () => {
        infoPopup.classList.remove('hidden');
    });

    // Close the info pop-up when "Close" is clicked
    closePopup.addEventListener('click', () => {
        infoPopup.classList.add('hidden');
    });
});

// Logout logic
document.getElementById('logoutButton')?.addEventListener('click', async () => {
    try {
        const response = await fetch('/logout', { method: 'POST' });
        const data = await response.json();
        alert(data.message);
        window.location.reload(); // Reload to reflect logged-out state
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Failed to log out. Please try again.');
    }
});



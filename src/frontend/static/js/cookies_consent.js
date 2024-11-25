// Ensure cookie consent logic is executed
document.addEventListener('DOMContentLoaded', () => {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');
    const infoButton = document.getElementById('infoButton');
    const infoPopup = document.getElementById('infoPopup');
    const closePopup = document.getElementById('closePopup');

    // Check cookie consent status from the server via session
    fetch('/cookie-status')
        .then(response => response.json())
        .then(data => {
            if (data.cookies_accepted) {
                console.log("Cookies already accepted. Hiding consent box.");
                cookieConsent.style.display = 'none'; // Hide cookie consent box
            } else {
                console.log("Showing cookie consent box.");
                cookieConsent.style.display = 'block'; // Show cookie consent box
            }
        })
        .catch(error => console.error('Error fetching cookie status:', error));

    // Handle "Accept Cookies" button click
    acceptCookies?.addEventListener('click', async () => {
        try {
            const response = await fetch('/accept-cookies', { method: 'POST' });
            const data = await response.json();
            console.log(data.message || "Cookies accepted by user.");
            cookieConsent.style.display = 'none'; // Hide cookie consent box
        } catch (error) {
            console.error('Error accepting cookies:', error);
        }
    });

    // Handle "Info" button click to show the popup
    infoButton?.addEventListener('click', () => {
        infoPopup?.classList.remove('hidden'); // Show info popup
    });

    // Handle "Close" button click to hide the popup
    closePopup?.addEventListener('click', () => {
        infoPopup?.classList.add('hidden'); // Hide info popup
    });
});

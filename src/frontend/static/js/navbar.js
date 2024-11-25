// Initialize navbar (if there are any interactive behaviors to manage)
document.addEventListener('DOMContentLoaded', () => {
    const navbarLinks = document.querySelectorAll('.top-menu a');

    // Example: Highlight the active link
    navbarLinks.forEach((link) => {
        link.addEventListener('click', () => {
            navbarLinks.forEach((link) => link.classList.remove('active')); // Remove active class
            link.classList.add('active'); // Add active class to the clicked link
        });
    });
});

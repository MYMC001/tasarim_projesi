document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');

    // Event listeners for switching tabs
    loginTab.addEventListener('click', function() {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
    });

    signupTab.addEventListener('click', function() {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
        signupTab.classList.add('active');
        loginTab.classList.remove('active');
    });
});
function toggleDropdown(event) {
    event.preventDefault(); // Prevent default anchor behavior
    const dropdownContent = event.currentTarget.nextElementSibling; // Get the dropdown content

    // Toggle display of dropdown content
    dropdownContent.style.display = (dropdownContent.style.display === "block") ? "none" : "block"; 
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-toggle')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].style.display = "none"; // Hide all dropdowns
        }
    }
}
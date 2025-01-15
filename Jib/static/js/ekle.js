// function displayCart() {
//     // Select the cart container
//     const cartContainer = document.querySelector('.cart-container');

//     // Toggle visibility of the cart
//     if (cartContainer.style.display === "none" || !cartContainer.style.display) {
//         cartContainer.style.display = "block"; // Show the cart
//     } else {
//         cartContainer.style.display = "block"; // Hide the cart if already visible
//     }
// }
function toggleForm() {
    var form = document.getElementById("product-form");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
document.getElementById('uploadButton').addEventListener('click', function() {
    document.getElementById('image').click();
});



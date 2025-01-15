let currentCardIndex = 0;
let cards;

document.addEventListener("DOMContentLoaded", function () {
  cards = document.querySelectorAll(".delivery-card");
  if (cards.length > 0) {
    cards[currentCardIndex].style.display = "block";
    startTimerForCard(currentCardIndex, 9);
  }
});

function updateTimer(cardIndex, countdown) {
  const timerElement = cards[cardIndex].querySelector(".delivery-card__timer");
  if (countdown > 0) {
    timerElement.textContent = `${countdown}s`;
    countdown--;
    timerInterval = setTimeout(() => updateTimer(cardIndex, countdown), 1000);
  } else {
    timerElement.textContent = "Expired";
    disableAcceptButton(cardIndex); 
    closeCard(); 
  }
}

function startTimerForCard(cardIndex, countdown) {
  updateTimer(cardIndex, countdown);
}

function disableAcceptButton(cardIndex) {
  const acceptButton = cards[cardIndex].querySelector('.delivery-card__accept-button');
  if (acceptButton) {
    acceptButton.disabled = true;
    acceptButton.textContent = "Expired";
  }
}

function closeCard() {
  if (cards[currentCardIndex]) {
    cards[currentCardIndex].style.display = "none"; 
  }

  currentCardIndex++;
  if (cards[currentCardIndex]) {
    cards[currentCardIndex].style.display = "block"; 
    startTimerForCard(currentCardIndex, 9); 
  }
}

function acceptOrder() {
  alert("Order Accepted!");
  location.reload();
}

function toggleOrders() {
  const orderSection = document.getElementById('wallet-order-section');
  if (orderSection.style.display === 'none') {
    orderSection.style.display = 'block';
  } else {
    orderSection.style.display = 'none';
  }
}

function withdrawFunds() {
  const balance = document.querySelector('.wallet-container__balance');
  const currentBalance = parseFloat(balance.innerText.replace('$', ''));
  if (currentBalance > 0) {
    balance.innerText = '$0.00'; 
    alert('You have successfully withdrawn your funds!');
  } else {
    alert('No funds available for withdrawal.');
  }
}

function requestPayout() {
  const balance = document.querySelector('.wallet-container__balance');
  const currentBalance = parseFloat(balance.innerText.replace('$', ''));
  if (currentBalance > 0) {
    alert('Your payout request has been submitted.');
  } else {
    alert('You have no balance to request a payout.');
  }
}


// JavaScript to toggle the visibility of the order items
document.addEventListener('DOMContentLoaded', () => {
  const viewDetailsBtn = document.getElementById('viewDetailsBtn');
  const orderItems = document.getElementById('orderItems');

  // Event listener for the "View Details" button
  viewDetailsBtn.addEventListener('click', () => {
    if (orderItems.style.display === 'none') {
      orderItems.style.display = 'block';
      viewDetailsBtn.textContent = 'Hide Details';
    } else {
      orderItems.style.display = 'none';
      viewDetailsBtn.textContent = 'View Details';
    }
  });
});

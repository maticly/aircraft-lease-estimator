// script.js

// Aircraft Selection
const aircraftGrid = document.querySelector('.aircraft-grid');
aircraftGrid.addEventListener('click', (event) => {
    if (event.target.tagName === 'SPAN') {
        const selectedAircraft = event.target.textContent;
        document.getElementById('selected-aircraft').value = selectedAircraft;
    }
});

// Airport Class Selection
const airportClassImages = document.querySelector('.airport-class-images');
airportClassImages.addEventListener('click', (event) => {
    if (event.target.tagName === 'SPAN') {
        const selectedClass = event.target.textContent;
        document.getElementById('selected-airport-class').value = selectedClass;
    }
});

// Economy Slider Updates 
const economySeatsSlider = document.getElementById('economy-seats');
const economySeatsDisplay = document.createElement('span');
economySeatsSlider.parentNode.insertBefore(economySeatsDisplay, economySeatsSlider.nextSibling);
economySeatsSlider.addEventListener('input', () => {
    economySeatsDisplay.textContent = economySeatsSlider.value;
});

// Business Slider Updates
const businessSeatsSlider = document.getElementById('business-seats');
const businessSeatsDisplay = document.createElement('span');
businessSeatsSlider.parentNode.insertBefore(businessSeatsDisplay, businessSeatsSlider.nextSibling);
businessSeatsSlider.addEventListener('input', () => {
    businessSeatsDisplay.textContent = businessSeatsSlider.value;
});

// Stopover Slider Updates
const stopoversSlider = document.getElementById('stopovers');
const stopoversDisplay = document.createElement('span');
stopoversSlider.parentNode.insertBefore(stopoversDisplay, stopoversSlider.nextSibling);
stopoversSlider.addEventListener('input', () => {
    stopoversDisplay.textContent = stopoversSlider.value;
});

// Form Submission
const leaseForm = document.getElementById('lease-form');
leaseForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = new FormData(leaseForm);

    // Send data to server (using Fetch API)
    fetch('/calculate-lease-price', { 
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display result
        document.getElementById('result').textContent = `Estimated Lease Price: $${data.price}`;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error (e.g., display an error message to the user)
    });
});

document.getElementById("calculate-distance").addEventListener("click", () => {
  const origin = document.getElementById("origin-airport").value;
  const destination = document.getElementById("destination-airport").value;

  if (!origin || !destination) {
    alert("Please enter both origin and destination airports.");
    return;
  }

  // API endpoint (replace with your Colab link)
  const apiUrl = "http://abcd-1234-5678.ngrok.io/calculate";

  // Make the POST request to your backend
  fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ origin, destination }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById("distance").value = data.distance;
        document.getElementById("flight-hours").value = data.flight_hours;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("There was an issue connecting to the backend.");
    });
});

// JavaScript for AI Trip Planner

document.addEventListener('DOMContentLoaded', function() {
    // Handle delete trip buttons
    const deleteButtons = document.querySelectorAll('.delete-trip');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tripId = this.getAttribute('data-trip-id');
            if (confirm('Are you sure you want to delete this trip?')) {
                fetch(`/delete_trip/${tripId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the trip card from the DOM
                        this.closest('.col-md-6').remove();
                        // If no trips left, show the no trips message
                        const tripCards = document.querySelectorAll('.col-md-6');
                        if (tripCards.length === 1) { // Since we removed one, check if now 0
                            location.reload(); // Simple way to refresh and show no trips
                        }
                    } else {
                        alert('Error deleting trip.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error deleting trip.');
                });
            }
        });
    });

    // Handle form submission for loading animation and AJAX
    const tripForm = document.getElementById('tripForm');
    if (tripForm) {
        tripForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent default form submission

            const planningDiv = document.getElementById('planning');
            const itineraryContainer = document.getElementById('itineraryContainer');

            if (planningDiv) {
                planningDiv.style.display = 'block';
            }
            if (itineraryContainer) {
                itineraryContainer.style.display = 'none';
            }

            // Collect form data
            const formData = new FormData(tripForm);

            // Send AJAX request
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    if (planningDiv) {
                        planningDiv.style.display = 'none';
                    }
                } else {
                    // Redirect to dashboard
                    window.location.href = `/dashboard/${data.trip_id}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
                if (planningDiv) {
                    planningDiv.style.display = 'none';
                }
            });
        });
    }
});

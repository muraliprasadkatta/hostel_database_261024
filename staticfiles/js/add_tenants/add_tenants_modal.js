// Function to fetch details like state, district, and city/town/village based on the provided pincode
function fetchPincodeDetails(pincode) {
    // Check if the pincode length is exactly 6 digits before making the request
    if (pincode.length === 6) {
        // Send an AJAX request to the Postal Pincode API to get the details
        $.ajax({
            url: `https://api.postalpincode.in/pincode/${pincode}`,  // API URL with the provided pincode
            method: 'GET',  // HTTP method for the request
            success: function (response) {
                // Check if the API returns a successful response
                if (response[0].Status === "Success") {
                    var postOffice = response[0].PostOffice[0];  // Extract the first post office's details
                    // Fill the input fields with the fetched state, district, and city/town/village
                    $('#input-search-box-state').val(postOffice.State); 
                    $('#input-search-box').val(postOffice.District);
                    $('#input-search-box-city').val(postOffice.Name);  // Set city/town/village
                } else {
                    alert("Invalid Pincode");  // Show an alert if the pincode is invalid
                }
            },
            error: function () {
                // Handle errors like network issues or API failure
                alert("An error occurred while fetching pincode details.");
            }
        });
    }
}

// Event listener to trigger fetchPincodeDetails function whenever the pincode input field changes
$('#input-search-box-pincode').on('input', function () {
    var pincode = $(this).val();  // Get the entered pincode value
    fetchPincodeDetails(pincode);  // Call the function to fetch the pincode details
});


// ----------------------------------------------

// Wait until the DOM content is fully loaded before executing this script
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('tenantForm');  // Get the form element by ID
    
    // Check if the form exists on the page
    if (form) {
        // Attach an event listener to handle the form submission
        form.addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent the default form submission (page reload)

            var formData = new FormData(this);  // Collect all the form data using FormData API

            // Use Fetch API to send the form data asynchronously
            fetch(this.action, {
                method: 'POST',  // Set the HTTP method to POST for form submission
                body: formData,  // Attach the collected form data
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Include the CSRF token for security
                }
            })
            .then(response => {
                if (!response.ok) {
                    // If the response is not successful, throw an error
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();  // Parse the JSON response
            })
            .then(data => {
                if (data.success) {
                    // If the data submission is successful, log success and refresh the page or perform other actions
                    console.log('Tenant successfully added/updated.');
                    location.reload();  // Optionally refresh the page after successful submission
                } else {
                    // If there is an error (e.g., validation errors), log and alert the user
                    console.error('Error:', data.error);
                    alert(data.error);  // Optionally alert the user with the error message
                }
            })
            .catch(error => {
                // Handle any errors during the Fetch request (e.g., network issues)
                console.error('Fetch error:', error);
            });
        });
    } else {
        // Log an error if the form with ID 'tenantForm' is not found on the page
        console.error("Form with id 'tenantForm' not found.");
    }
});

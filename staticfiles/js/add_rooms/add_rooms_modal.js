document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('roomForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting the traditional way

            var formData = new FormData(this); // Collect the form data

            // Send the form data via Fetch API
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Include the CSRF token
                }
            })
            .then(response => {
                if (!response.ok) {
                    // Handle errors if the response is not OK (e.g., 400 or 500 errors)
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json(); // Parse JSON response if successful
            })
            .then(data => {
                if (data.success) {
                    console.log('Room successfully added or updated.');
                    // Reload the page after successful form submission
                    location.reload();
                } else {
                    // If there's an error in the form, display it
                    console.error('Error:', data.error);
                    alert(data.error); // Optionally alert the user
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                // Handle fetch errors (e.g., network issues)
            });
        });
    } else {
        console.error("Form with id 'roomForm' not found."); // If the form is not found
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Enable the "Add Room" button when the page is ready
    $('#add-room-button').prop('disabled', false);

    // Open the "Add Room" modal when the button is clicked
    $('#add-room-button').on('click', function () {
        $('#addRoomModal').css('display', 'block'); // Show the modal
        $(this).prop('disabled', true); // Disable the button to prevent double-click
        setTimeout(() => {
            $(this).prop('disabled', false); // Re-enable the button after 1 second
        }, 1000);
    });

    // Close the modal when the "X" button is clicked
    $('.close').on('click', function () {
        $('#addRoomModal').css('display', 'none');
    });

    // Close the modal if the user clicks outside of it
    $(window).on('click', function (event) {
        if (event.target.id === 'addRoomModal') {
            $('#addRoomModal').css('display', 'none');
        }
    });

    // Function to load room data when editing a room
    window.editRoom = function (roomNumber) {
        var roomData = user_rooms.find(room => room.room_number == roomNumber); // Find the room data by room number
        if (roomData) {
            // Populate the form with the room data
            $('#room_id').val(roomData.id);
            $('#roomnumber').val(roomData.room_number);
            $('#floortype').val(roomData.floor_type);
            $('#numberofshare').val(roomData.number_of_share);
            $('#remarks').val(roomData.remarks);

            // Update the occupied beds field
            var occupiedBeds = roomData.has_data;
            $('#current_occupied_beds').val(occupiedBeds);

            // Set the radio buttons for availability
            if (roomData.available_room_or_not === 'yes') {
                $('#available_yes').prop('checked', true);
            } else {
                $('#available_no').prop('checked', true);
            }

            // Set the checkboxes for room facilities
            $('input[name="transportation"]').prop('checked', false); // Uncheck all facilities
            roomData.room_facilities.split(', ').forEach(function (facility) {
                $('input[name="transportation"][value="' + facility + '"]').prop('checked', true); // Check the corresponding facility
            });

            // Show the modal
            $('#addRoomModal').css('display', 'block');
        }
    };

    // Toggle the display of options menu for each room
    window.toggleOptions = function (roomNumber) {
        var menu = document.getElementById("optionsMenu_" + roomNumber);
        if (menu.style.display === "none" || menu.style.display === "") {
            menu.style.display = "block"; // Show the menu
        } else {
            menu.style.display = "none"; // Hide the menu
        }
    };

    // Function to select or deselect all room facilities
    window.toggleSelectAll = function () {
        var selectAllChecked = document.getElementById('select_all').checked; // Check if the "Select All" checkbox is checked
        var checkboxes = document.querySelectorAll('input[name="transportation"]'); // Get all facility checkboxes
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = selectAllChecked; // Set each checkbox to match the "Select All" checkbox
        });
    };

    // Close dropdowns when clicking outside
    window.onclick = function (event) {
        if (!event.target.matches('.fas') && !event.target.matches('.room-edit-option')) {
            var dropdowns = document.getElementsByClassName("room-edit-options-menu");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none"; // Hide the dropdown
                }
            }
        }
    };
});

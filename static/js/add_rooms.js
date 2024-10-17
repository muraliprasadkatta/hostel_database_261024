     
    function printError(Id, Msg) {
        document.getElementById(Id).innerHTML = Msg;
    }
    function validateForm() {
    
        var roomnumber = document.Form.roomnumber.value;
        var floortype = document.Form.floortype.value;
        var numberofshare = document.Form.numberofshare.value
        var rent = document.Form.rent.value;
        var advance = document.Form.advance.value;

        var roomnumberErr = false;
        var floortypeErr = false;
        var numberofshareErr = false;
        var rentErr = false;
        var advanceErr = false;

        
        // var roomnumberErr = floortypeErr = numberofshareErr = rentErr = advanceErr  =  false;
    
        if (roomnumber === null || roomnumber.trim() === "") {
            printError("roomnumberErr", "Please enter a room number");
            var elem = document.getElementById("roomnumber");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
            roomnumberErr = true;
        } else {
            var regex = /^\d{1,6}$/; // Adjusted regex to enforce exactly 6 digits
            if (regex.test(roomnumber) === false) {
                printError("roomnumberErr", "Please enter a valid room number or given below 6 digits");
                var elem = document.getElementById("roomnumber");
                elem.classList.add("input-2");
                elem.classList.remove("input-1");
                roomnumberErr = true;
            } else {
                printError("roomnumberErr", "");
                var elem = document.getElementById("roomnumber");
                elem.classList.add("input-1");
                elem.classList.remove("input-2");
            }      
        }
        
        if (floortype === null || floortype.trim() === "") {
            printError("floortypeErr", "Please enter a room number");
            var elem = document.getElementById("floortype");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
            floortypeErr = true;
        } else {
            var regex = /^\d{1,6}$/; // Adjusted regex to enforce exactly 6 digits
            if (regex.test(floortype) === false) {
                printError("floortypeErr", "Please enter a valid room number or given below 6 digits");
                var elem = document.getElementById("floortype");
                elem.classList.add("input-2");
                elem.classList.remove("input-1");
                floortypeErr = true;
            } else {
                printError("floortypeErr", "");
                var elem = document.getElementById("floortype");
                elem.classList.add("input-1");
                elem.classList.remove("input-2");
            }
        }
        
    
        if (numberofshare === null || numberofshare.trim() === "") {
            printError("numberofshareErr", "Please enter a number of shares");
            var elem = document.getElementById("numberofshare");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
            numberofshareErr = true;
        } else {
            var regex = /^\d+$/;
            if (regex.test(numberofshare) === false) {
                printError("numberofshareErr", "Please enter a valid number");
                var elem = document.getElementById("numberofshare");
                elem.classList.add("input-2");
                elem.classList.remove("input-1");
                numberofshareErr = true;
            } else {
                printError("numberofshareErr", "");
                var elem = document.getElementById("numberofshare");
                elem.classList.add("input-1");
                elem.classList.remove("input-2");
            }
        }
    
        if (rent === null || rent.trim() === "") {
            printError("rentErr", "Please enter a valid input (100 or 200 or 300)");
            var elem = document.getElementById("rent");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
            rentErr = true;
        } else {
            var regex = /^[1-9][0-9]*$/;
            if(regex.test(rent) === false) {
                printError("rentErr", "Please enter a valid input (100 or 200 or 300)");
                var elem = document.getElementById("rent");
                elem.classList.add("input-2");
                elem.classList.remove("input-1");
                feeErr = true;
            } else {
                printError("rentErr", "");
                var elem = document.getElementById("rent");
                elem.classList.add("input-1");
                elem.classList.remove("input-2");
            }
        }
    
        if (advance === null || advance.trim() === "") {
            printError("advanceErr", "Please enter your input number");
            var elem = document.getElementById("advance");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
            advanceErr = true;
        } else {
            var regex = /^[0-9]+$/;
            if(regex.test(advance) === false) {
                printError("advanceErr", "Please enter a valid number");
                var elem = document.getElementById("advance");
                elem.classList.add("input-2");
                elem.classList.remove("input-1");
                advanceErr = true;
            } else {
                printError("advanceErr", "");
                var elem = document.getElementById("advance");
                elem.classList.add("input-1");
                elem.classList.remove("input-2");
            }
        }
            // Check for errors in all fields
    if (roomnumberErr || floortypeErr || numberofshareErr || rentErr || advanceErr) {
        return false; // Prevent form submission if there are errors
    }

    return true; // Allow form submission if there are no errors
}


  

// prevent the form re-submmition
   
window.onload = function() {
    // Check if the form was just submitted and the session flag is set
    if (sessionStorage.getItem("formSubmitted")) {
        // Alert the user that they are being redirected because the form was already submitted
        alert('Redirecting to avoid duplicate submission.');
        // Redirect to the desired URL or perform other appropriate action
        window.location.href = '{% url "DisplayRooms" property_id=selected_property.id %}';
    }
};

document.querySelector('form').addEventListener('submit', function(e) {
    // Prevent the form from submitting normally
    e.preventDefault();
    // Perform form validation or other checks here
    if (validateForm()) {
        // Simulate form submission, e.g., via AJAX or setting window.location
        // Example: submitFormViaAjax();
        // Set the session flag only after successful submission
        sessionStorage.setItem("formSubmitted", "true");
        // Optionally redirect or reload the page to show submission results
        window.location.reload(); // Or redirect as needed
    }
});

// Function to call when navigating to the form via "Add Another Room" button
function goToFormPage() {
    sessionStorage.removeItem("formSubmitted"); // Ensure the flag is cleared when opening the form normally
    window.location.href = '{% url "AddRooms" property_id=selected_property.id %}';
}

// Bind this function to your "Add Another Room" button
document.getElementById('addAnotherRoomButton').addEventListener('click', goToFormPage);

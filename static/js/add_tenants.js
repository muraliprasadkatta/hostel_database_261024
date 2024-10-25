function printError(Id, Msg) {
    document.getElementById(Id).innerHTML = Msg;
}

function validateForm() {

    var name = document.Form.name.value;
    var ownername = document.Form.ownername.value
    var email = document.Form.email.value;
    var mobile = document.Form.mobile.value;
    var address = document.Form.address.value
    // var country = document.Form.country.value;
    // var gender = document.Form.gender.value;
    

    var nameErr = ownernameErr = emailErr = mobileErr = addressErr = true;
    

    if (name === null || name.trim() === "") {
        printError("nameErr", "Please enter your name");
        var elem = document.getElementById("name");
        elem.classList.add("input-2");
        elem.classList.remove("input-1");
    } else {
        var regex = /^[a-zA-Z\s]+$/;                
        if (regex.test(name) === false) {
            printError("nameErr", "Please enter a valid name");
            var elem = document.getElementById("name");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
        } else {
            printError("nameErr", "");
            hostelnameErr = false;
            var elem = document.getElementById("name");
            elem.classList.add("input-1");
            elem.classList.remove("input-2");
        }
    }
    
    if (ownername === null || ownername.trim() === "") {
        printError("ownernameErr", "Please enter owner name");
        var elem = document.getElementById("ownername");
        elem.classList.add("input-2");
        elem.classList.remove("input-1");
    } else {
        var regex = /^[a-zA-Z\s]+$/;                
        if (regex.test(ownername) === false) {
            printError("ownernameErr", "Please enter a valid owner name");
            var elem = document.getElementById("ownername");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
        } else {
            printError("ownernameErr", "");
            ownernameErr = false;
            var elem = document.getElementById("ownername");
            elem.classList.add("input-1");
            elem.classList.remove("input-2");
        }
    }
    
    
    if(email == "") {
        printError("emailErr", "Please enter your email address");
         var elem = document.getElementById("email");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
    } else {
        
        var regex = /^.*@gmail\.com$/;
        if(regex.test(email) === false) {
            printError("emailErr", "Please enter a valid email address");
            var elem = document.getElementById("email");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
        } else{
            printError("emailErr", "");
            emailErr = false;
            var elem = document.getElementById("email");
            elem.classList.add("input-1");
            elem.classList.remove("input-2");

        }
    }
    
 
    if(mobile == "") {
        printError("mobileErr", "Please enter your mobile number");
        var elem = document.getElementById("mobile");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
    } else {
        var regex = /^[1-9]\d{9}$/;
        if(regex.test(mobile) === false) {
            printError("mobileErr", "Please enter a valid 10 digit mobile number");
            var elem = document.getElementById("mobile");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
        } else{
            printError("mobileErr", "");
            mobileErr = false;
            var elem = document.getElementById("mobile");
            elem.classList.add("input-1");
            elem.classList.remove("input-2");
        }
    }
    if (address.trim() === "") {
        printError("addressErr", "Please enter your valid address");
        var elem = document.getElementById("address");
        elem.classList.add("input-2");
        elem.classList.remove("input-1");
    } else {
        var regex = /^[a-zA-Z0-9\s,'-]*$/;
        if (regex.test(address) === false) {
            printError("addressErr", "Please enter a valid pattern");
            var elem = document.getElementById("address");
            elem.classList.add("input-2");
            elem.classList.remove("input-1");
        } else {
            printError("addressErr", "");
            addressErr = false;
            var elem = document.getElementById("address");
            elem.classList.add("input-1");
            elem.classList.remove("input-2");
        }
    }
    

    // if(country == "Select") {
    //     printError("countryErr", "Please select your country");
    //     var elem = document.getElementById("country");
    //         elem.classList.add("input-4");
    //         elem.classList.remove("input-3");
    // } else {
    //     printError("countryErr", "");
    //     countryErr = false;
    //     var elem = document.getElementById("country");
    //         elem.classList.add("input-3");
    //         elem.classList.remove("input-4");
    // }
    

    // if(gender == "") {
    //     printError("genderErr", "Please select your gender");
    //     var elem = document.getElementById("gender");
    //         elem.classList.add("input-4");
    //         elem.classList.remove("input-3");
    // } else {
    //     printError("genderErr", "");
    //     genderErr = false;
    //     var elem = document.getElementById("gender");
    //         elem.classList.add("input-3");
    //         elem.classList.remove("input-4");
    // }
    
    
    if((hostelnameErr || ownernameErr ||  emailErr || mobileErr || adressErr) == true) {
       return false;
    } 
};
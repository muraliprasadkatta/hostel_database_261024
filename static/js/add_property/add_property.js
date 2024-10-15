    // Toggle sidebar function
    function toggleSidebar() {
        var sidebar = document.getElementById('sidebar');
        var mainContainer = document.getElementById('main-container');
        var header = document.getElementById('header');
        var menuIcon = document.getElementById('menuIcon');
        var headerContent = document.getElementById('headerContent');
        var contentContainer = document.getElementById('main-content');

        sidebar.classList.toggle('open');
        mainContainer.classList.toggle('compressed');
        header.classList.toggle('compressed');
        contentContainer.classList.toggle('compressed');

        if (sidebar.classList.contains('open')) {
            menuIcon.classList.add('hidden');
            if (window.innerWidth <= 768) {
                headerContent.classList.add('mobile-hidden');
            }
        } else {
            menuIcon.classList.remove('hidden');
            headerContent.classList.remove('mobile-hidden');
        }
    }

    // Open/Close Add Property Modal
    function openAddPropertyModal() {
        document.getElementById('addPropertyModal').style.display = 'block';
        document.getElementById('main-container').classList.add('blur');
        document.getElementById('header').classList.add('blur');

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function closeAddPropertyModal() {
        document.getElementById('addPropertyModal').style.display = 'none';
        document.getElementById('main-container').classList.remove('blur');
        document.getElementById('header').classList.remove('blur');
    }

    // Handle Geolocation Success and Errors
    function showPosition(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('latitude').value = latitude;
        document.getElementById('longitude').value = longitude;
    }

    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert("User denied the request for Geolocation.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Location information is unavailable.");
                break;
            case error.TIMEOUT:
                alert("The request to get user location timed out.");
                break;
            case error.UNKNOWN_ERROR:
                alert("An unknown error occurred.");
                break;
        }
    }

    // Set Profile Photo Modal: Camera Access and File Upload
    function openAddPropertyCameraAccessModal() {
        document.getElementById('cameraAccessModal').style.display = 'block';
    }

    function closeAddPropertyCameraAccessModal(event) {
        event.stopPropagation();
        document.getElementById('cameraAccessModal').style.display = 'none';
    }

    function displayFileNameAndClose(input) {
        const fileName = input.files[0].name;
        const truncatedFileName = fileName.length > 15 ? fileName.substring(0, 15) + '...' : fileName;
        const setProfilePhotoButton = document.querySelector('button[onclick="openAddPropertyCameraAccessModal()"]');
        setProfilePhotoButton.textContent = `File: ${truncatedFileName}`;
        closeAddPropertyCameraAccessModal(new Event('click'));

        const reader = new FileReader();
        reader.onload = function(e) {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.classList.remove('image-preview-camera');
            imagePreview.src = e.target.result;
            document.getElementById('imagePreviewContainer').style.display = 'flex';
        }
        reader.readAsDataURL(input.files[0]);
    }

    // Camera Functions: Open, Capture, and Close
    function openAddPropertyCamera() {
        const cameraModal = document.getElementById('cameraModal');
        const video = document.getElementById('video');
        const cameraAccessModal = document.getElementById('cameraAccessModal');
        cameraAccessModal.style.display = 'none';
        cameraModal.style.display = 'block';
        startCamera();
    }

    function closeAddPropertyCameraModal(event) {
        event.stopPropagation();
        const cameraModal = document.getElementById('cameraModal');
        const video = document.getElementById('video');
        if (currentStream) {
            const tracks = currentStream.getTracks();
            tracks.forEach(track => track.stop());
        }
        video.srcObject = null;
        cameraModal.style.display = 'none';
    }

    function startCamera() {
        const video = document.getElementById('video');

        navigator.mediaDevices.enumerateDevices()
            .then(devices => {
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                const rearCamera = videoDevices.find(device => device.label.toLowerCase().includes('back'));
                const constraints = {
                    video: {
                        deviceId: rearCamera ? rearCamera.deviceId : (videoDevices[0] ? videoDevices[0].deviceId : undefined),
                        facingMode: rearCamera ? { exact: 'environment' } : 'user'
                    }
                };

                navigator.mediaDevices.getUserMedia(constraints)
                    .then(stream => {
                        currentStream = stream;
                        video.srcObject = stream;
                    })
                    .catch(err => {
                        console.error("Error accessing the camera: ", err);
                        alert("An error occurred while accessing the camera.");
                    });
            })
            .catch(err => {
                console.error("Error enumerating devices: ", err);
                alert("An error occurred while accessing camera devices.");
            });
    }

    function flipCamera() {
        const video = document.getElementById('video');
        navigator.mediaDevices.enumerateDevices()
            .then(devices => {
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                const rearCamera = videoDevices.find(device => device.label.toLowerCase().includes('back'));

                if (useFrontCamera) {
                    if (rearCamera) {
                        useFrontCamera = false;
                        startCamera();
                    } else {
                        alert("No rear camera found. Using front camera.");
                    }
                } else {
                    useFrontCamera = true;
                    startCamera();
                }
            })
            .catch(err => {
                console.error("Error enumerating devices: ", err);
                alert("An error occurred while accessing camera devices.");
            });
    }

    function takeSnapshot() {
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            const file = new File([blob], "snapshot.jpg", { type: 'image/jpeg' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.getElementById('imageUpload').files = dataTransfer.files;
            closeAddPropertyCameraModal(new Event('click'));
            displayCameraPreview(document.getElementById('imageUpload'));
        }, 'image/jpeg');
    }

    function displayCameraPreview(input) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.classList.add('image-preview-camera');
            imagePreview.src = e.target.result;
            document.getElementById('imagePreviewContainer').style.display = 'flex';
        }
        reader.readAsDataURL(input.files[0]);
    }

    function retakePhoto() {
        document.getElementById('imagePreviewContainer').style.display = 'none';
        openAddPropertyCameraAccessModal();
    }

    // Pin Modal and PIN Input Logic
    document.addEventListener('DOMContentLoaded', function() {
        const setPinButton = document.querySelector('button[onclick="openPinModal()"]');
        if (setPinButton) {
            setPinButton.addEventListener('click', function(event) {
                event.preventDefault();
                openPinModal();
            });
        }
    });

    function openPinModal() {
        document.getElementById('pinModal').style.display = 'flex';
    }

    function closePinModal() {
        document.getElementById('pinModal').style.display = 'none';
    }

    function checkPinInput() {
        const pinInput = document.getElementById('managementPin');
        const setPinButton = document.getElementById('setPinButton');
        if (pinInput && setPinButton) {
            if (pinInput.value) {
                setPinButton.classList.add('pin-success');
                setPinButton.textContent = 'Set PIN Success';
            } else {
                setPinButton.classList.remove('pin-success');
                setPinButton.textContent = 'Set PIN';
            }
        }
    }

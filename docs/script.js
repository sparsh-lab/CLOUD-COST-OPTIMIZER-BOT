// Main script file for Cloud Cost Optimizer web app

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // --- Entry Page Functionality ---
    const enterButton = document.getElementById('enterBtn');
    const gestureOverlay = document.getElementById('gesture-overlay');
    
    if (enterButton) {
        console.log("Enter button found, attaching event listener");
        
        enterButton.addEventListener('click', function() {
            console.log("Enter button clicked");
            
            // Show gesture overlay
            if (gestureOverlay) {
                gestureOverlay.classList.add('show');
                console.log("Showing gesture overlay");
                
                // Navigate to dashboard page after gesture animation
                setTimeout(function() {
                    console.log("Navigating to dashboard.html");
                    window.location.href = 'dashboard.html';
                }, 1500);
            } else {
                // Direct navigation if overlay not found
                console.log("Gesture overlay not found, navigating directly");
                window.location.href = 'dashboard.html';
            }
        });
    }
    
    // --- Dashboard Page Functionality ---
    const emailButton = document.getElementById('emailBtn');
    const pageGesture = document.getElementById('page-gesture');
    
    // Show entrance gesture on dashboard page load
    if (pageGesture) {
        console.log("Dashboard page gesture found");
        
        // Show and then hide the gesture indicator
        pageGesture.classList.add('show');
        setTimeout(function() {
            pageGesture.classList.remove('show');
        }, 2000);
    }
    
    // Email button functionality
    if (emailButton) {
        console.log("Email button found, attaching event listener");
        
        emailButton.addEventListener('click', function() {
            console.log("Email button clicked");
            const statusElement = document.getElementById('emailStatus');
            
            // Disable button and show loading state
            emailButton.disabled = true;
            emailButton.innerText = 'Sending...';
            
            // Call AWS API function
            sendEmailViaAWS()
                .then(function(response) {
                    console.log("Email sent successfully", response);
                    
                    // Show success message
                    statusElement.classList.add('success');
                    statusElement.classList.remove('error');
                    statusElement.innerText = 'Report sent successfully!';
                    emailButton.innerText = 'Send Report via Email';
                    emailButton.disabled = false;
                })
                .catch(function(error) {
                    console.error("Failed to send email", error);
                    
                    // Show error message
                    statusElement.classList.add('error');
                    statusElement.classList.remove('success');
                    statusElement.innerText = 'Failed to send report. Please try again.';
                    emailButton.innerText = 'Send Report via Email';
                    emailButton.disabled = false;
                });
        });
    }
});

// AWS API Integration Function
function sendEmailViaAWS() {
    console.log("Attempting to send email via AWS API");

    // Call the AWS API endpoint using fetch
    return fetch('https://0a1gvq2q93.execute-api.ap-south-1.amazonaws.com/webapp', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
            // Add any required headers here, e.g., Authorization
        },
        body: JSON.stringify({ email: 'sparshkmr17@gmail.com', report: '...' })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw {
                    success: false,
                    message: 'Failed to send email',
                    error: err,
                    timestamp: new Date().toISOString()
                };
            });
        }
        return response.json().then(data => ({
            success: true,
            message: 'Email sent successfully',
            data: data,
            timestamp: new Date().toISOString()
        }));
    })
    .catch(error => {
        throw {
            success: false,
            message: 'Failed to send email',
            error: error,
            timestamp: new Date().toISOString()
        };
    });
}



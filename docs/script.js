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
    
    // ========== REPLACE THIS SECTION WITH YOUR AWS API CODE ==========
    // This is a placeholder function that simulates an API call
    // Replace with your actual AWS API integration code
    
    return new Promise((resolve, reject) => {
        // Simulating network request with 1.5 second delay
        console.log("Making API request to AWS...");
        
        setTimeout(() => {
            // Simulate 80% success rate for testing
            if (Math.random() < 0.8) {
                resolve({
                    success: true,
                    message: 'Email sent successfully',
                    timestamp: new Date().toISOString()
                });
            } else {
                reject({
                    success: false,
                    message: 'Failed to send email',
                    error: 'API Error 403: Unauthorized',
                    timestamp: new Date().toISOString()
                });
            }
        }, 1500);
    });
    // ========== END OF SECTION TO REPLACE ==========
}

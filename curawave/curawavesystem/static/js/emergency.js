document.addEventListener('DOMContentLoaded', function() {
    const emergencyBtn = document.querySelector('.emergency-btn');
    
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', function(e) {
            // Check if it's a mobile device
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                // Mobile device will handle the tel: protocol automatically
                return true;
            } else {
                e.preventDefault();
                // Show alert on desktop devices
                alert('Emergency Number: 112\nPlease call from your phone for immediate assistance.');
            }
        });
    }
});

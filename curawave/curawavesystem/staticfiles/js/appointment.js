document.addEventListener('DOMContentLoaded', function() {
    const timeInput = document.getElementById('appointmentTime');
    const dateInput = document.getElementById('appointmentDate');
    const form = document.getElementById('appointmentForm');

    // Generate time slots every 30 minutes between 9 AM and 5 PM
    function generateTimeSlots() {
        const slots = [];
        for (let hour = 9; hour < 17; hour++) {
            slots.push(`${hour.toString().padStart(2, '0')}:00`);
            slots.push(`${hour.toString().padStart(2, '0')}:30`);
        }
        return slots;
    }

    // Initialize datalist for time slots
    if (timeInput) {
        const timeList = document.createElement('datalist');
        timeList.id = 'timeSlots';
        const slots = generateTimeSlots();
        slots.forEach(time => {
            const option = document.createElement('option');
            option.value = time;
            timeList.appendChild(option);
        });
        timeInput.setAttribute('list', 'timeSlots');
        document.body.appendChild(timeList);
    }

    // Date validation
    if (dateInput) {
        // Set minimum date to today
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        dateInput.min = `${yyyy}-${mm}-${dd}`;

        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const dayOfWeek = selectedDate.getDay();

            // Validate weekday selection
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                alert('Please select a weekday (Monday-Friday)');
                this.value = '';
            }
        });
    }

    // Time validation
    if (timeInput) {
        timeInput.addEventListener('change', function() {
            const selectedTime = this.value;
            const [hours] = selectedTime.split(':').map(Number);

            // Validate business hours
            if (hours < 9 || hours >= 17) {
                alert('Please select a time between 9:00 AM and 5:00 PM');
                this.value = '';
            }
        });
    }

    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!dateInput.value || !timeInput.value) {
                e.preventDefault();
                alert('Please select both date and time for your appointment');
                return;
            }

            const selectedDateTime = new Date(`${dateInput.value} ${timeInput.value}`);
            if (selectedDateTime < new Date()) {
                e.preventDefault();
                alert('Please select a future date and time');
                return;
            }
        });
    }
});
 // Background images array
 const images = [
            "{{ url_for('static', filename='images/auction1.jpg') }}",
            "{{ url_for('static', filename='images/auction2.jpg') }}",
            "{{ url_for('static', filename='images/auction3.jpeg') }}"
        ];

        let currentIndex = 0;

        // Function to change background image
        function changeBackground() {
            document.body.style.backgroundImage = `url(${images[currentIndex]})`;
            currentIndex = (currentIndex + 1) % images.length; // Cycle through images
        }

        // Change background every 5 seconds
        setInterval(changeBackground, 5000);

        // Initial background setup
        changeBackground();

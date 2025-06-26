// Menu Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.fixed-nav')) {
            navMenu.classList.remove('active');
        }
    });
});

// Slideshow Functionality
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    let currentSlide = 0;

    // Initialize first slide
    if (slides.length > 0) {
        slides[0].classList.add('active');
    }

    function showSlide(n) {
        // Remove active class from all slides
        slides.forEach(slide => slide.classList.remove('active'));
        
        // Calculate the index
        currentSlide = (n + slides.length) % slides.length;
        
        // Add active class to current slide
        slides[currentSlide].classList.add('active');
    }

    // Event listeners for prev/next buttons
    if (prevButton && nextButton) {
        prevButton.addEventListener('click', () => {
            showSlide(currentSlide - 1);
        });

        nextButton.addEventListener('click', () => {
            showSlide(currentSlide + 1);
        });
    }

    // Auto advance slides every 5 seconds
    setInterval(() => {
        showSlide(currentSlide + 1);
    }, 5000);
}); 
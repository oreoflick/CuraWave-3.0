(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    // Initiate the wowjs
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 40) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Counter animation
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

    // Initialize counter-up
    const counterElements = document.querySelectorAll('[data-toggle="counter-up"]');
    counterElements.forEach(element => {
        new Waypoint({
            element: element,
            handler: function() {
                const target = parseInt(element.getAttribute('data-toggle-target')) || 0;
                let count = 0;
                const updateCounter = () => {
                    const increment = target / 20;
                    count = Math.ceil(count + increment);
                    if (count < target) {
                        element.textContent = count;
                        setTimeout(updateCounter, 100);
                    } else {
                        element.textContent = target;
                    }
                };
                updateCounter();
                this.destroy();
            },
            offset: '90%'
        });
    });

    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
        nav: false,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn'
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav: false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });

    // Add smooth scrolling to all links
    $("a").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Service item hover effect
    $('.service-item').hover(function() {
        $(this).find('.service-icon').addClass('rotate-icon');
    }, function() {
        $(this).find('.service-icon').removeClass('rotate-icon');
    });

    // Doctor card hover effect
    $('.doctor-card').hover(function() {
        $(this).find('img').addClass('scale-image');
    }, function() {
        $(this).find('img').removeClass('scale-image');
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Search form interactions
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[type="text"]');
        const submitBtn = searchForm.querySelector('button[type="submit"]');

        searchInput.addEventListener('focus', () => {
            searchForm.classList.add('focused');
        });

        searchInput.addEventListener('blur', () => {
            searchForm.classList.remove('focused');
        });

        searchForm.addEventListener('submit', (e) => {
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Searching...';
            submitBtn.disabled = true;
        });
    }

    // Add animations to counters
    const counterBoxes = document.querySelectorAll('.counter-box');
    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-float');
            }
        });
    }, observerOptions);

    counterBoxes.forEach(box => {
        observer.observe(box);
    });

    // Emergency button pulse animation
    const emergencyBtn = document.querySelector('.emergency-btn');
    if (emergencyBtn) {
        setInterval(() => {
            emergencyBtn.classList.add('pulse');
            setTimeout(() => {
                emergencyBtn.classList.remove('pulse');
            }, 1000);
        }, 3000);
    }

})(jQuery);


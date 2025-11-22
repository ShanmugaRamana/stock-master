document.addEventListener("DOMContentLoaded", function () {
    
    // SCROLL ANIMATIONS
    const animateElements = document.querySelectorAll('.hidden-left, .hidden-right, .hidden-up');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show-view');
            } else {
                // Remove class to reset animation so it plays again on scroll
                entry.target.classList.remove('show-view');
            }
        });
    }, {
        threshold: 0.15
    });

    animateElements.forEach((el) => {
        observer.observe(el);
    });
});
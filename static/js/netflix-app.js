// Netflix-style Portfolio JavaScript

// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.querySelector('.netflix-header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Slider functionality
function slideLeft(sliderId) {
    const slider = document.getElementById(sliderId);
    const cardWidth = 295; // card width + gap
    slider.scrollBy({
        left: -cardWidth * 3,
        behavior: 'smooth'
    });
}

function slideRight(sliderId) {
    const slider = document.getElementById(sliderId);
    const cardWidth = 295; // card width + gap
    slider.scrollBy({
        left: cardWidth * 3,
        behavior: 'smooth'
    });
}

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Card hover effects and interactions
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add hover effect
            this.style.zIndex = '20';
        });
        
        card.addEventListener('mouseleave', function() {
            // Remove hover effect
            this.style.zIndex = '1';
        });
    });
});

// Keyboard navigation for sliders
document.addEventListener('keydown', function(e) {
    const activeSlider = document.querySelector('.row-slider:hover');
    if (activeSlider) {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            const sliderId = activeSlider.id;
            slideLeft(sliderId);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            const sliderId = activeSlider.id;
            slideRight(sliderId);
        }
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.content-row, .about-section, .cta-section');
    animateElements.forEach(el => {
        observer.observe(el);
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .content-row, .about-section, .cta-section {
        opacity: 0;
    }
`;
document.head.appendChild(style);

// Mobile menu toggle (if needed in future)
function toggleMobileMenu() {
    const nav = document.querySelector('.main-nav');
    nav.classList.toggle('mobile-open');
}

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized scroll handler
const optimizedScrollHandler = debounce(function() {
    const header = document.querySelector('.netflix-header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}, 10);

window.addEventListener('scroll', optimizedScrollHandler);
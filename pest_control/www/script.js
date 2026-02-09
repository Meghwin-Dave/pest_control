/**
 * ARBITER PEST CONTROL - JAVASCRIPT
 * Handles form submissions, interactions, and dynamic features
 */

// ========================================
// DOCUMENT READY
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeScrollAnimations();
    initializeFormHandlers();
    initializeMegaMenu();
});

// ========================================
// FORM HANDLING
// ========================================

function initializeFormHandlers() {
    const contactForm = document.getElementById('contactForm');
    const quoteForm = document.getElementById('quoteForm');

    if (contactForm) {
        contactForm.addEventListener('submit', handleContactFormSubmit);
    }

    if (quoteForm) {
        quoteForm.addEventListener('submit', handleQuoteFormSubmit);
    }
}

function handleContactFormSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        service: document.getElementById('service').value,
        message: document.getElementById('message').value
    };

    // Validate form
    if (!validateForm(formData)) {
        showMessage('contactForm', 'Please fill in all required fields correctly.', 'error');
        return;
    }

    // Simulate form submission
    submitForm(formData, 'contactForm', 'contact');
}

function handleQuoteFormSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('quoteName').value,
        email: document.getElementById('quoteEmail').value,
        phone: document.getElementById('quotePhone').value,
        service: document.getElementById('quoteService').value,
        details: document.getElementById('quoteDetails').value
    };

    // Validate form
    if (!validateForm(formData)) {
        showMessage('quoteForm', 'Please fill in all required fields correctly.', 'error');
        return;
    }

    // Simulate form submission
    submitForm(formData, 'quoteForm', 'quote');
}

function validateForm(data) {
    // Check if all required fields are filled
    for (let key in data) {
        if (!data[key] || data[key].trim() === '') {
            return false;
        }
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        return false;
    }

    // Validate phone format (basic validation)
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    if (!phoneRegex.test(data.phone)) {
        return false;
    }

    return true;
}

function submitForm(data, formId, type) {
    const form = document.getElementById(formId);
    const messageDiv = document.getElementById(formId === 'contactForm' ? 'formMessage' : 'quoteMessage');
    const submitButton = form.querySelector('button[type="submit"]');

    // Disable submit button and show loading state
    submitButton.disabled = true;
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';

    // Simulate API call with timeout
    setTimeout(() => {
        // Success message
        showMessage(formId, 'Thank you! We\'ve received your ' + type + ' request. Our team will contact you within 24 hours.', 'success');

        // Reset form
        form.reset();

        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.innerHTML = originalText;

        // Close modal if it's the quote form
        if (formId === 'quoteForm') {
            const modal = bootstrap.Modal.getInstance(document.getElementById('quoteModal'));
            if (modal) {
                setTimeout(() => {
                    modal.hide();
                }, 2000);
            }
        }

        // Scroll to message
        setTimeout(() => {
            messageDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }, 1500);
}

function showMessage(formId, message, type) {
    const messageDiv = document.getElementById(formId === 'contactForm' ? 'formMessage' : 'quoteMessage');
    messageDiv.style.display = 'block';
    messageDiv.className = 'alert alert-' + (type === 'success' ? 'success' : 'danger') + ' alert-dismissible fade show';
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
}

// ========================================
// SCROLL ANIMATIONS
// ========================================

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    document.querySelectorAll('.service-card, .industry-card, .testimonial-card, .feature-item').forEach(el => {
        observer.observe(el);
    });
}

// ========================================
// EVENT LISTENERS
// ========================================

function initializeEventListeners() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Close mobile menu if open
                const navbar = document.querySelector('.navbar-collapse');
                if (navbar.classList.contains('show')) {
                    const toggler = document.querySelector('.navbar-toggler');
                    toggler.click();
                }
            }
        });
    });

    // Add active class to nav links on scroll
    window.addEventListener('scroll', updateActiveNavLink);

    // Handle navbar background on scroll
    window.addEventListener('scroll', handleNavbarScroll);
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    // Only handle in-page anchor navigation links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');

    if (!navLinks.length) {
        return;
    }

    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href && href.slice(1) === current) {
            link.classList.add('active');
        }
    });
}

function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
    }
}

// ========================================
// MEGA MENU
// ========================================

function initializeMegaMenu() {
    const megaToggles = document.querySelectorAll('.nav-item.has-mega > .mega-toggle, .nav-item.has-mega > .nav-link.mega-toggle');

    megaToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // On desktop we rely on hover; click is primarily for mobile
            if (window.innerWidth < 992) {
                e.preventDefault();
                const parentItem = this.closest('.nav-item.has-mega');
                const isOpen = parentItem.classList.contains('mega-open');

                document.querySelectorAll('.nav-item.has-mega.mega-open').forEach(item => {
                    if (item !== parentItem) {
                        item.classList.remove('mega-open');
                    }
                });

                if (!isOpen) {
                    parentItem.classList.add('mega-open');
                } else {
                    parentItem.classList.remove('mega-open');
                }
            }
        });
    });

    // Close mega menus when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth >= 992) return;
        const nav = document.querySelector('.navbar-premium');
        if (!nav.contains(e.target)) {
            document.querySelectorAll('.nav-item.has-mega.mega-open').forEach(item => {
                item.classList.remove('mega-open');
            });
        }
    });
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Format phone number for display
 */
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

/**
 * Debounce function for scroll events
 */
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

/**
 * Add animation class on scroll
 */
const animateOnScroll = debounce(() => {
    document.querySelectorAll('.service-card, .industry-card').forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;

        if (elementTop < window.innerHeight && elementBottom > 0) {
            element.style.animation = 'slideInUp 0.6s ease-out forwards';
        }
    });
}, 100);

window.addEventListener('scroll', animateOnScroll);

// ========================================
// INITIALIZATION
// ========================================

// Initialize tooltips if Bootstrap is available
document.addEventListener('DOMContentLoaded', function() {
    if (typeof bootstrap !== 'undefined') {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
});

// ========================================
// PERFORMANCE OPTIMIZATION
// ========================================

// Lazy load images if supported
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}

// ========================================
// ACCESSIBILITY ENHANCEMENTS
// ========================================

// Ensure all interactive elements are keyboard accessible
document.addEventListener('keydown', function(event) {
    // Close modals on Escape key
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        });
    }
});

// ========================================
// ANALYTICS TRACKING (Optional)
// ========================================

/**
 * Track user interactions for analytics
 */
function trackEvent(eventName, eventData) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    } else if (typeof _gaq !== 'undefined') {
        _gaq.push(['_trackEvent', 'Interaction', eventName, JSON.stringify(eventData)]);
    }
    // Log to console for debugging
    console.log('Event tracked:', eventName, eventData);
}

// Track button clicks
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
        trackEvent('button_click', {
            button_text: this.textContent.trim(),
            button_class: this.className
        });
    });
});

// Track form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        trackEvent('form_submit', {
            form_id: this.id,
            form_name: this.name
        });
    });
});

// ========================================
// EXPORT FUNCTIONS FOR EXTERNAL USE
// ========================================

window.ArbitePestControl = {
    formatPhoneNumber: formatPhoneNumber,
    trackEvent: trackEvent,
    submitForm: submitForm,
    validateForm: validateForm
};

console.log('Arbiter Pest Control website initialized successfully!');
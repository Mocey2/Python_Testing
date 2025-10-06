/* ========================================
   GUDLFT - DYNAMIC INTERACTIONS
   ======================================== */

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeFormEnhancements();
    initializeDynamicEffects();
    initializeResponsiveFeatures();
});

// ===== ANIMATION INITIALIZATION =====
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .competition-card, .club-card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add slide-in animation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach((form, index) => {
        form.classList.add('slide-in-up');
        form.style.animationDelay = `${index * 0.2}s`;
    });

    // Add floating animation to header
    const header = document.querySelector('.header');
    if (header) {
        header.classList.add('floating');
    }
}

// ===== FORM ENHANCEMENTS =====
function initializeFormEnhancements() {
    // Enhanced form validation with real-time feedback
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        // Add focus/blur effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            validateField(this);
        });

        // Real-time validation
        input.addEventListener('input', function() {
            validateField(this);
        });
    });

    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add ripple effect
            createRippleEffect(e, this);
            
            // Add loading state for form submissions
            if (this.type === 'submit') {
                addLoadingState(this);
            }
        });
    });
}

// ===== DYNAMIC EFFECTS =====
function initializeDynamicEffects() {
    // Dynamic background
    const body = document.body;
    body.classList.add('dynamic-bg');

    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('.btn, .competition-card, .club-card');
    interactiveElements.forEach(element => {
        element.classList.add('hover-lift');
    });

    // Add glow effects to important elements
    const importantElements = document.querySelectorAll('.points-display, .alert-success');
    importantElements.forEach(element => {
        element.classList.add('glow-success');
    });

    // Add error glow to error elements
    const errorElements = document.querySelectorAll('.alert-error');
    errorElements.forEach(element => {
        element.classList.add('glow-error');
    });
}

// ===== RESPONSIVE FEATURES =====
function initializeResponsiveFeatures() {
    // Mobile menu toggle (if needed)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }

    // Responsive animations
    window.addEventListener('resize', debounce(handleResize, 250));
}

// ===== UTILITY FUNCTIONS =====

// Field validation
function validateField(field) {
    const value = field.value.trim();
    const fieldGroup = field.parentElement;
    
    // Remove existing validation classes
    fieldGroup.classList.remove('valid', 'invalid');
    
    if (field.hasAttribute('required') && !value) {
        fieldGroup.classList.add('invalid');
        return false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            fieldGroup.classList.add('invalid');
            return false;
        }
    }
    
    // Number validation
    if (field.type === 'number' && value) {
        const num = parseFloat(value);
        const min = parseFloat(field.getAttribute('min')) || 0;
        const max = parseFloat(field.getAttribute('max')) || Infinity;
        
        if (isNaN(num) || num < min || num > max) {
            fieldGroup.classList.add('invalid');
            return false;
        }
    }
    
    if (value) {
        fieldGroup.classList.add('valid');
    }
    
    return true;
}

// Ripple effect for buttons
function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Loading state for buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.classList.add('loading');
    button.disabled = true;
    
    // Remove loading state after form submission (if not prevented)
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('loading');
        button.disabled = false;
    }, 2000);
}

// Mobile menu toggle
function toggleMobileMenu() {
    const menu = document.querySelector('.mobile-menu');
    if (menu) {
        menu.classList.toggle('active');
    }
}

// Handle window resize
function handleResize() {
    // Adjust animations based on screen size
    const isMobile = window.innerWidth < 768;
    const cards = document.querySelectorAll('.competition-card, .club-card');
    
    cards.forEach(card => {
        if (isMobile) {
            card.classList.remove('hover-lift');
        } else {
            card.classList.add('hover-lift');
        }
    });
}

// Debounce function
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

// ===== DYNAMIC CONTENT UPDATES =====

// Update points display with animation
function updatePointsDisplay(newPoints) {
    const pointsDisplay = document.querySelector('.points-display');
    if (pointsDisplay) {
        pointsDisplay.classList.add('pulse');
        setTimeout(() => {
            pointsDisplay.textContent = `Points available: ${newPoints}`;
            pointsDisplay.classList.remove('pulse');
        }, 300);
    }
}

// Show success message with animation
function showSuccessMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success bounce-in';
    alert.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        setTimeout(() => {
            alert.classList.add('zoom-out');
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    }
}

// Show error message with animation
function showErrorMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-error shake';
    alert.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        setTimeout(() => {
            alert.classList.add('zoom-out');
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    }
}

// ===== COMPETITION STATUS UPDATES =====

// Update competition status with animation
function updateCompetitionStatus(competitionElement, newStatus) {
    const statusElement = competitionElement.querySelector('.competition-status');
    if (statusElement) {
        statusElement.classList.add('flip-in');
        setTimeout(() => {
            statusElement.className = `competition-status status-${newStatus}`;
            statusElement.classList.remove('flip-in');
        }, 400);
    }
}

// ===== PROGRESS INDICATORS =====

// Show progress bar
function showProgress(percentage) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const progressFill = progressBar.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.setProperty('--progress-width', `${percentage}%`);
            progressBar.style.display = 'block';
        }
    }
}

// Hide progress bar
function hideProgress() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.display = 'none';
    }
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Escape key to close modals or clear forms
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            activeModal.classList.remove('active');
        }
    }
    
    // Enter key to submit forms
    if (e.key === 'Enter' && e.target.classList.contains('form-control')) {
        const form = e.target.closest('form');
        if (form) {
            form.submit();
        }
    }
});

// ===== ACCESSIBILITY ENHANCEMENTS =====

// Add focus indicators for keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// ===== PERFORMANCE OPTIMIZATIONS =====

// Lazy load images (if any are added later)
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
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
}

// Initialize lazy loading
lazyLoadImages();

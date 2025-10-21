// =======================================================
// E-Hospitality Main JavaScript File
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('E-Hospitality System Loaded Successfully! 🏥');
    
    // ===================================
    // 1. AUTO-DISMISS ALERTS
    // ===================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            try {
                bsAlert.close();
            } catch (error) {
                // Alert already closed or doesn't exist
            }
        }, 5000);
    });

    // ===================================
    // 2. CONFIRM DELETE ACTIONS
    // ===================================
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const confirmMessage = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });

    // Also handle links with onclick="return confirm()"
    const confirmLinks = document.querySelectorAll('a[onclick*="confirm"]');
    confirmLinks.forEach(link => {
        // These already have inline confirm, no need to add more
        console.log('Confirm link found:', link.textContent);
    });

    // ===================================
    // 3. FORM VALIDATION
    // ===================================
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // ===================================
    // 4. DATE PICKER RESTRICTIONS
    // ===================================
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        // Set minimum date to today for appointment dates
        if (input.name === 'appointment_date' || input.hasAttribute('data-min-today')) {
            input.setAttribute('min', today);
        }
        
        // Set maximum date for birth dates (no future dates)
        if (input.name === 'date_of_birth') {
            input.setAttribute('max', today);
        }
    });

    // ===================================
    // 5. TABLE SEARCH FUNCTIONALITY
    // ===================================
    const searchInputs = document.querySelectorAll('[data-table-search]');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const tableId = this.getAttribute('data-table-search');
            const table = document.getElementById(tableId);
            if (!table) return;

            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const cells = row.getElementsByTagName('td');
                let found = false;
                
                for (let j = 0; j < cells.length; j++) {
                    if (cells[j].textContent.toLowerCase().includes(filter)) {
                        found = true;
                        break;
                    }
                }
                
                row.style.display = found ? '' : 'none';
            });
        });
    });

    // ===================================
    // 6. TOOLTIP INITIALIZATION
    // ===================================
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ===================================
    // 7. SMOOTH SCROLL FOR ANCHOR LINKS
    // ===================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===================================
    // 8. PRINT FUNCTIONALITY
    // ===================================
    const printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // ===================================
    // 9. DYNAMIC TIME SLOT SELECTION
    // ===================================
    const timeSlots = document.querySelectorAll('.time-slot');
    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            // Remove selected class from all slots
            timeSlots.forEach(s => s.classList.remove('selected', 'bg-primary', 'text-white'));
            
            // Add selected class to clicked slot
            this.classList.add('selected', 'bg-primary', 'text-white');
            
            // Update hidden input if exists
            const timeInput = document.getElementById('appointment_time');
            if (timeInput) {
                timeInput.value = this.getAttribute('data-time');
            }
        });
    });

    // ===================================
    // 10. FORM AUTO-SAVE INDICATOR
    // ===================================
    const autoSaveForms = document.querySelectorAll('[data-autosave]');
    autoSaveForms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                showNotification('Changes detected', 'info');
            });
        });
    });

    // ===================================
    // 11. DYNAMIC APPOINTMENT STATUS COLORS
    // ===================================
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(badge => {
        const text = badge.textContent.toLowerCase();
        if (text.includes('scheduled') || text.includes('pending')) {
            badge.classList.add('bg-warning');
        } else if (text.includes('completed') || text.includes('paid')) {
            badge.classList.add('bg-success');
        } else if (text.includes('cancelled')) {
            badge.classList.add('bg-danger');
        }
    });

    // ===================================
    // 12. PASSWORD STRENGTH INDICATOR
    // ===================================
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name.includes('password1') || input.id.includes('password1')) {
            input.addEventListener('keyup', function() {
                const strength = checkPasswordStrength(this.value);
                showPasswordStrength(this, strength);
            });
        }
    });

    // ===================================
    // 13. REAL-TIME FORM VALIDATION
    // ===================================
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.classList.add('is-invalid');
                showFieldError(this, 'Please enter a valid email address');
            } else {
                this.classList.remove('is-invalid');
                removeFieldError(this);
            }
        });
    });

    // ===================================
    // 14. DASHBOARD CARD ANIMATIONS
    // ===================================
    const dashboardCards = document.querySelectorAll('.dashboard-card, .card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    dashboardCards.forEach(card => {
        observer.observe(card);
    });

    // ===================================
    // 15. MOBILE MENU CLOSE ON LINK CLICK
    // ===================================
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });

    // ===================================
    // 16. INITIALIZE POPOVERS
    // ===================================
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // ===================================
    // 17. LOADING SPINNER FOR FORMS
    // ===================================
    const formsWithSubmit = document.querySelectorAll('form');
    formsWithSubmit.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && this.checkValidity()) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Submit';
                }, 5000);
            }
        });
    });

});

// =======================================================
// UTILITY FUNCTIONS
// =======================================================

// Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Format date helper
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Format time helper
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

// Check password strength
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;
    return strength;
}

// Show password strength
function showPasswordStrength(input, strength) {
    let strengthText = '';
    let strengthClass = '';
    
    if (strength <= 1) {
        strengthText = 'Weak';
        strengthClass = 'text-danger';
    } else if (strength <= 3) {
        strengthText = 'Medium';
        strengthClass = 'text-warning';
    } else {
        strengthText = 'Strong';
        strengthClass = 'text-success';
    }
    
    let strengthIndicator = input.parentElement.querySelector('.password-strength');
    if (!strengthIndicator) {
        strengthIndicator = document.createElement('small');
        strengthIndicator.className = 'password-strength d-block mt-1';
        input.parentElement.appendChild(strengthIndicator);
    }
    
    strengthIndicator.className = `password-strength d-block mt-1 ${strengthClass}`;
    strengthIndicator.textContent = `Password strength: ${strengthText}`;
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show field error
function showFieldError(input, message) {
    let errorDiv = input.parentElement.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Remove field error
function removeFieldError(input) {
    const errorDiv = input.parentElement.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// AJAX form submission helper
function submitFormAjax(formId, successCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                if (successCallback) successCallback(data);
            } else {
                showNotification(data.message, 'danger');
            }
        })
        .catch(error => {
            showNotification('An error occurred', 'danger');
            console.error('Error:', error);
        });
    });
}

// Print specific element
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'danger');
    });
}

// Scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
window.addEventListener('scroll', function() {
    let scrollButton = document.getElementById('scrollToTopBtn');
    
    if (!scrollButton) {
        scrollButton = document.createElement('button');
        scrollButton.id = 'scrollToTopBtn';
        scrollButton.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4';
        scrollButton.style.display = 'none';
        scrollButton.style.zIndex = '9999';
        scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollButton.onclick = scrollToTop;
        document.body.appendChild(scrollButton);
    }
    
    if (window.pageYOffset > 300) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
});

console.log('All E-Hospitality JavaScript functions loaded! ✅');

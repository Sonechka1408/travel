document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const inputs = form.querySelectorAll('input');
    const submitButton = form.querySelector('button[type="submit"]');

    // Custom validation messages
    const validationMessages = {
        firstName: {
            pattern: 'First name must start with a capital letter followed by lowercase letters',
            required: 'First name is required'
        },
        lastName: {
            pattern: 'Last name must start with a capital letter followed by lowercase letters',
            required: 'Last name is required'
        },
        email: {
            pattern: 'Please enter a valid email address',
            required: 'Email is required'
        },
        phone: {
            pattern: 'Phone number must be in format: +7XXXXXXXXXX',
            required: 'Phone number is required'
        },
        password: {
            pattern: 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character',
            required: 'Password is required',
            minLength: 'Password must be at least 8 characters long'
        },
        confirmPassword: {
            required: 'Please confirm your password',
            match: 'Passwords do not match'
        }
    };

    // Validate single input
    function validateInput(input) {
        const errorElement = input.nextElementSibling;
        let isValid = true;

        // Reset error message
        errorElement.textContent = '';

        // Required validation
        if (input.required && !input.value) {
            errorElement.textContent = validationMessages[input.name].required;
            isValid = false;
        }

        // Pattern validation
        else if (input.pattern && input.value) {
            const regex = new RegExp(input.pattern);
            if (!regex.test(input.value)) {
                errorElement.textContent = validationMessages[input.name].pattern;
                isValid = false;
            }
        }

        // Email validation
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                errorElement.textContent = validationMessages.email.pattern;
                isValid = false;
            }
        }

        // Password confirmation
        if (input.name === 'confirmPassword') {
            const password = document.getElementById('password');
            if (input.value !== password.value) {
                errorElement.textContent = validationMessages.confirmPassword.match;
                isValid = false;
            }
        }

        // Update input validity state
        input.classList.toggle('is-invalid', !isValid);
        input.classList.toggle('is-valid', isValid);

        return isValid;
    }

    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            validateInput(input);
            updateSubmitButton();
        });

        input.addEventListener('blur', () => {
            validateInput(input);
            updateSubmitButton();
        });
    });

    // Update submit button state
    function updateSubmitButton() {
        let isFormValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isFormValid = false;
            }
        });
        submitButton.disabled = !isFormValid;
    }

    // Form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        let isValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            // Here you would typically send the data to a server
            alert('Registration successful!');
            form.reset();
        }
    });

    // Initial validation state
    updateSubmitButton();
}); 
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

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea');
        const submitButton = form.querySelector('button[type="submit"]');

        function validateInput(input) {
            const errorElement = input.nextElementSibling;
            let isValid = true;

            if (input.required && !input.value.trim()) {
                errorElement.textContent = `${input.name} is required`;
                isValid = false;
            }

            // Name validation
            if (input.name === 'name' || input.name === 'first_name' || input.name === 'last_name') {
                const nameRegex = /^[A-Z][a-z]+$/;
                if (!nameRegex.test(input.value)) {
                    errorElement.textContent = 'Must start with a capital letter followed by lowercase letters';
                    isValid = false;
                }
            }

            // Email validation
            if (input.type === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(input.value)) {
                    errorElement.textContent = 'Please enter a valid email address';
                    isValid = false;
                }
            }

            // Phone validation
            if (input.name === 'phone') {
                const phoneRegex = /^\+7\d{10}$/;
                if (!phoneRegex.test(input.value)) {
                    errorElement.textContent = 'Phone number must be in format: +7XXXXXXXXXX';
                    isValid = false;
                }
            }

            // Password validation
            if (input.type === 'password' && input.name === 'password') {
                const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
                if (!passwordRegex.test(input.value)) {
                    errorElement.textContent = 'Password must have 8+ characters, uppercase, lowercase, number and special character';
                    isValid = false;
                }
            }

            // Confirm password
            if (input.name === 'confirm_password') {
                const password = form.querySelector('input[name="password"]');
                if (input.value !== password.value) {
                    errorElement.textContent = 'Passwords do not match';
                    isValid = false;
                }
            }

            input.classList.toggle('is-invalid', !isValid);
            input.classList.toggle('is-valid', isValid);

            return isValid;
        }

        // Real-time validation
        inputs.forEach(input => {
            ['input', 'blur'].forEach(eventType => {
                input.addEventListener(eventType, () => {
                    validateInput(input);
                    if (submitButton) {
                        let formValid = true;
                        inputs.forEach(input => {
                            if (!validateInput(input)) {
                                formValid = false;
                            }
                        });
                        submitButton.disabled = !formValid;
                    }
                });
            });
        });

        // Form submission
        form.addEventListener('submit', function(event) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
}); 
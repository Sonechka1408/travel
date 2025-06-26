document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const statusMessage = document.getElementById('statusMessage');

    // Replace these with your actual Telegram Bot API credentials
    const TELEGRAM_BOT_TOKEN = '8099365862:AAGk5FkSB6h1cIInzUnNwMNs9a3xlclsU1E';
    const TELEGRAM_CHAT_ID = '8099365862';
  

    // Validate single input
    function validateInput(input) {
        const errorElement = input.nextElementSibling;
        let isValid = true;

        // Reset error message
        errorElement.textContent = '';

        // Required validation
        if (input.required && !input.value.trim()) {
            errorElement.textContent = `${input.name} is required`;
            isValid = false;
        }

        // Pattern validation for name
        if (input.name === 'name' && input.value) {
            const nameRegex = /^[A-Za-z\s]{2,50}$/;
            if (!nameRegex.test(input.value)) {
                errorElement.textContent = 'Please enter a valid name (2-50 characters, letters only)';
                isValid = false;
            }
        }

        // Email validation
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                errorElement.textContent = 'Please enter a valid email address';
                isValid = false;
            }
        }

        // Length validation for subject and message
        if ((input.name === 'subject' || input.name === 'message') && input.value) {
            if (input.value.length < input.minLength) {
                errorElement.textContent = `Minimum ${input.minLength} characters required`;
                isValid = false;
            }
            if (input.value.length > input.maxLength) {
                errorElement.textContent = `Maximum ${input.maxLength} characters allowed`;
                isValid = false;
            }
        }

        // Update input validity state
        input.classList.toggle('is-invalid', !isValid);
        input.classList.toggle('is-valid', isValid);

        return isValid;
    }

    // Show status message
    function showStatus(message, isError = false) {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message ' + (isError ? 'error' : 'success');
        statusMessage.style.display = 'block';

        // Hide message after 5 seconds
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    }

    // Send message to Telegram
    async function sendToTelegram(formData) {
        const message = `
New Contact Form Message:
Name: ${formData.get('name')}
Email: ${formData.get('email')}
Subject: ${formData.get('subject')}
Message: ${formData.get('message')}
        `.trim();

        try {
            const response = await fetch(TELEGRAM_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chat_id: TELEGRAM_CHAT_ID,
                    text: message,
                    parse_mode: 'HTML'
                })
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            return true;
        } catch (error) {
            console.error('Error sending message:', error);
            return false;
        }
    }

    // Form submission handler
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Validate all inputs
        let isValid = true;
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            showStatus('Please fix the errors in the form', true);
            return;
        }

        // Disable submit button and show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';

        // Get form data
        const formData = new FormData(form);

        // Send to Telegram
        const success = await sendToTelegram(formData);

        if (success) {
            showStatus('Message sent successfully! We\'ll get back to you soon.');
            form.reset();
        } else {
            showStatus('Failed to send message. Please try again later.', true);
        }

        // Reset button state
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    });

    // Real-time validation
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        ['input', 'blur'].forEach(eventType => {
            input.addEventListener(eventType, () => validateInput(input));
        });
    });
}); 
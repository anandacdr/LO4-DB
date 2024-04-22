document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('call-form');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form); // Gather form data
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        try {
            const response = await fetch('/submit-call', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                throw new Error('Failed to submit call details');
            }

            // Optionally, handle the success response here
            console.log('Call details submitted successfully');
            form.reset(); // Clear the form
        } catch (error) {
            console.error('Error:', error.message);
        }
    });
});

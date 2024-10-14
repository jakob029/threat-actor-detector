document.getElementById('textInputForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way
    
    const prompt = document.getElementById('promptInput').value;  // Get the input value
    
    if (prompt) {
        const formData = new FormData();  // Create form data object
        formData.append('prompt', prompt);  // Append the input to the form data
        
        fetch('/analyze', {  // Send a POST request to the '/analyze' endpoint
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            const resultDiv = document.getElementById('result');  // Get the result div
            resultDiv.innerHTML = `<p>Response: ${data.response}</p>`;  // Display the response
        })
        .catch(error => {
            console.error('Error:', error);  // Handle any errors
            document.getElementById('result').innerHTML = `<p>Error fetching response.</p>`;
        });
    }
});

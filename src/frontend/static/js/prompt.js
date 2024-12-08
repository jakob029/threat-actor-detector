document.getElementById('textInputForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const promptInput = document.getElementById('promptInput');
    const responseContainer = document.getElementById('responseContainer');
    const loader = document.getElementById('loader');
    const responseText = document.getElementById('responseText');

    const promptText = promptInput.value;

    if (promptText) {
        promptInput.value = '';
        responseContainer.classList.add('visible');
        loader.style.display = 'block';
        responseText.innerHTML = '';

        try {
            // Explicitly call /conversations first
            const conversationResponse = await fetch('/conversations', { method: 'POST' });
            const conversationData = await conversationResponse.json();

            if (!conversationResponse.ok || !conversationData.cid) {
                throw new Error(conversationData.message || "Failed to create conversation.");
            }

            console.log(`Conversation created with cid: ${conversationData.cid}`);

            // Proceed with /analyze
            const formData = new FormData();
            formData.append('prompt', promptText);

            const analyzeResponse = await fetch('/analyze', {
                method: 'POST',
                body: formData,
            });

            const analyzeData = await analyzeResponse.json();
            loader.style.display = 'none';

            if (analyzeResponse.ok) {
                // Use marked.parse() to convert Markdown to HTML
                const dirtyHTML = marked.parse(analyzeData.response);
                // Sanitize the HTML to prevent XSS attacks
                const cleanHTML = DOMPurify.sanitize(dirtyHTML);
                // Display the sanitized HTML
                responseText.innerHTML = cleanHTML;

                // Initialize syntax highlighting
                document.querySelectorAll('#responseText pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                // Handle data_points if needed
                const dataPoints = analyzeData.data_points;
                console.log("Data points received for chart:", dataPoints);

                if (dataPoints && Object.keys(dataPoints).length > 0) {
                    document.getElementById("chartContainer").style.display = "block";
                    renderChart(dataPoints);
                } else {
                    console.error("No data points available for chart rendering.");
                    document.getElementById("chartContainer").style.display = "none";
                }
            } else {
                responseText.innerHTML = `<p>${analyzeData.response || "Error analyzing prompt."}</p>`;
            }
        } catch (error) {
            console.error('Error:', error);
            loader.style.display = 'none';
            responseText.innerHTML = `<p>${error.message || "Error fetching response."}</p>`;
        }
    }
});

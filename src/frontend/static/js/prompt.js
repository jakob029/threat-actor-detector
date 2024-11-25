// Handle prompt submission
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
            const formData = new FormData();
            formData.append('prompt', promptText);

            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            loader.style.display = 'none';
            responseText.innerHTML = `${data.response.replace(/\n/g, '<br>')}`;

            const dataPoints = data.data_points;
            if (dataPoints && Object.keys(dataPoints).length > 0) {
                document.getElementById("chartContainer").style.display = "block";
                renderChart(dataPoints); // Assumes `renderChart` is globally accessible
            } else {
                console.error("No data points available for chart rendering.");
                document.getElementById("chartContainer").style.display = "none";
            }
        } catch (error) {
            console.error('Error:', error);
            loader.style.display = 'none';
            responseText.innerHTML = '<p>Error fetching response.</p>';
        }
    }
});

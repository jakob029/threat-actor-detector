// Initialize Chart.js and set up a global chart instance variable
let chartInstance = null;

function renderChart(dataPoints) {
    const ctx = document.getElementById("dataGraph").getContext("2d");

    // Extract labels and values from the data points
    const labels = Object.keys(dataPoints); 
    const values = Object.values(dataPoints); 

    // Destroy any existing chart instance before creating a new one
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Create a new Chart.js instance
    chartInstance = new Chart(ctx, {
        type: 'bar', // Bar chart type
        data: {
            labels: labels,
            datasets: [{
                label: 'Analysis Data',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.2)', 
                borderColor: 'rgba(54, 162, 235, 1)', 
                borderWidth: 1 
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true, 
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

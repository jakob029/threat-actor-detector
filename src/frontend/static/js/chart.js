let chartInstance = null;

function renderChart(dataPoints) {
    const ctx = document.getElementById("dataGraph").getContext("2d");

    if (!ctx) {
        console.error('Chart canvas element not found');
        return;
    }

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(dataPoints),
            datasets: [{
                label: 'Analysis Result',
                data: Object.values(dataPoints),
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
                        callback: (value) => value + '%'
                    }
                }
            }
        }
    });
}

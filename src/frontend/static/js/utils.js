// Format JSON data into HTML for display
function formatJsonData(jsonData) {
    let html = '<ul>';
    for (const [key, value] of Object.entries(jsonData)) {
        if (typeof value === 'object' && value !== null) {
            html += `<li><strong>${key}:</strong> ${formatJsonData(value)}</li>`;
        } else {
            html += `<li><strong>${key}:</strong> ${value}</li>`;
        }
    }
    html += '</ul>';
    return html;
}

// Allow "Enter" to submit the form, but "Shift+Enter" creates a new line
document.getElementById('promptInput')?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        document.getElementById('textInputForm').requestSubmit();
    }
});
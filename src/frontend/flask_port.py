from flask import Flask, request, jsonify, render_template
import requests

# Initialize the Flask app
app = Flask(__name__)

# Route to render the homepage
@app.route('/')
def homepage():
    return render_template('Homepage.html')  # Ensure Homepage.html is in the templates folder

# Route to handle the input prompt
@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the prompt from the form data
    prompt = request.form.get('prompt')
    
    print(f"Received prompt: {prompt}")
    
    if not prompt:
        return jsonify({'response': 'No prompt received'})

    # Oollama server URL and payload
    oollama_url = "http://100.77.88.10/api/generate"
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        print(f"Sending payload to Oollama: {payload}")
        
        response = requests.post(oollama_url, json=payload, headers=headers)
        response_data = response.json()
        
        print(f"Oollama server response: {response_data}")

        # Adjust this to correctly access the 'response' key from Oollama's result
        return jsonify({'response': response_data.get('response', 'No result')})
    
    except Exception as e:
        print(f"Error communicating with Oollama server: {e}")
        return jsonify({'response': f'Error communicating with Oollama server: {str(e)}'})

# Ensure that the Flask app runs when the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)

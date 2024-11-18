"""Flask api for sending and receiving prompts, user support and sessions."""

from flask import Flask, request, jsonify, render_template, session
import requests

# Initialize the Flask app
app = Flask(__name__)

# Define a single base URL for all API requests
BASE_URL = "http://100.77.88.40:5000"

# Set a secret key for session management
app.secret_key = "Jeppecool1"


@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    """Route to handle cookies in the API."""
    session["cookies_accepted"] = True
    return jsonify({"message": "Cookies accepted"})


@app.route("/")
def homepage():
    """Route to home page."""
    print(f"Session on homepage: {session}")  # Debug log
    cookies_accepted = session.get("cookies_accepted", False)
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template(
        "Homepage.html", is_logged_in=is_logged_in, username=session.get("username"), cookies_accepted=cookies_accepted
    )


@app.route("/info.html")
def info_page():
    """Route to info page."""
    print(f"Session on info page: {session}")  # Debug log
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template("info.html", is_logged_in=is_logged_in, username=session.get("username"))


# Route to handle user login
@app.route("/user/login", methods=["POST"])
def login():
    """Login function to handle users."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        response = requests.post(f"{BASE_URL}/user/login", json={"username": username, "password": password})
        response_data = response.json()

        if response_data.get("message") == "success":
            # Clear any existing session
            session.clear()

            # Store new user information in the session
            session["uid"] = response_data.get("uid")
            session["username"] = username
            print(f"New session set: uid={session['uid']}, username={session['username']}")
            return jsonify({"message": "success"})
        else:
            return jsonify({"message": response_data.get("message")})
    except Exception as e:
        return jsonify({"message": f"Error communicating with the authentication server: {str(e)}"})


# Route to handle user registration
@app.route("/user/register", methods=["POST"])
def register():
    """Route to handle user registers."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        response = requests.post(f"{BASE_URL}/user/register", json={"username": username, "password": password})
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"message": f"Error communicating with the registration server: {str(e)}"})


# Route to handle the input prompt
@app.route("/analyze", methods=["POST"])
def analyze():
    """Main prompt route to retrieve and send requests to the LLM."""
    prompt = request.form.get("prompt")

    if not prompt:
        return jsonify({"response": "No prompt received"})

    # Use the BASE_URL for the analysis endpoint
    analyze_url = f"{BASE_URL}/analyzis"
    payload = {"prompt": prompt}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(analyze_url, json=payload, headers=headers)
        response_data = response.json()
        return jsonify({"response": response_data.get("response", "No result")})
    except Exception as e:
        return jsonify({"response": f"Error communicating with the analysis server: {str(e)}"})


# Route to handle user logout
@app.route("/logout", methods=["POST"])
def logout():
    """Route to end user session and sign out."""
    session.clear()  # Clears all session data
    return jsonify({"message": "Logged out successfully"})


# Ensure that the Flask app runs when the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)

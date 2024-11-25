"""Flask API for managing user sessions, prompts, and interactions with an LLM backend."""

from flask import Flask, request, jsonify, render_template, session
import requests

# Initialize the Flask app
app = Flask(__name__)

# Define a single base URL for all API requests
BASE_URL = "http://100.77.88.40:5000"

#  Key for session management
app.secret_key = "Jeppecool1"  


@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    """
    Handle cookie consent acceptance.

    This route marks the user's session as having accepted cookies.

    Returns:
        dict: JSON response confirming the action.
    """
    session["cookies_accepted"] = True
    return jsonify({"message": "Cookies accepted"})


@app.route("/")
def homepage():
    """
    Render the homepage.

    Displays information about user session status, including whether cookies
    have been accepted and whether the user is logged in.

    Returns:
        str: Rendered template for the homepage.
    """
    cookies_accepted = session.get("cookies_accepted", False)
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template(
        "homepage.html",
        is_logged_in=is_logged_in,
        username=session.get("username"),
        cookies_accepted=cookies_accepted,
    )


@app.route("/info.html")
def info_page():
    """
    Render the info page.

    Displays information about the application or user.

    Returns:
        str: Rendered template for the info page.
    """
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template(
        "info.html", is_logged_in=is_logged_in, username=session.get("username")
    )


@app.route("/user/login", methods=["POST"])
def login():
    """
    Handle user login.

    Sends login credentials to the backend API and updates the session on success.

    Returns:
        dict: JSON response with success or error message.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        response = requests.post(
            f"{BASE_URL}/user/login", json={"username": username, "password": password}
        )
        response_data = response.json()

        if response_data.get("message") == "success":
            # Clear any existing session
            session.clear()
            # Store new user information in the session
            session["uid"] = response_data.get("uid")
            session["username"] = username
            return jsonify({"message": "success"})

        return jsonify({"message": response_data.get("message")})
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})


@app.route("/user/register", methods=["POST"])
def register():
    """
    Handle user registration.

    Sends registration details to the backend API.

    Returns:
        dict: JSON response with success or error message.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        response = requests.post(
            f"{BASE_URL}/user/register", json={"username": username, "password": password}
        )
        return jsonify(response.json())
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a prompt using the LLM backend.

    Forwards the user-provided prompt to the backend and returns the analysis result.

    Returns:
        dict: JSON response containing the LLM's response and any related data points.
    """
    prompt = request.form.get("prompt")
    if not prompt:
        return jsonify({"response": "No prompt received"})

    analyze_url = f"{BASE_URL}/analyzis"
    payload = {"prompt": prompt}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(analyze_url, json=payload, headers=headers)
        response_data = response.json()
        return jsonify(
            {
                "response": response_data.get("response", "No result"),
                "data_points": response_data.get("data_points", {}),
            }
        )
    except requests.RequestException as err:
        return jsonify({"response": f"Error communicating with the server: {str(err)}"})


@app.route("/logout", methods=["POST"])
def logout():
    """
    Log out the current user.

    Clears the session data to log out the user.

    Returns:
        dict: JSON response confirming the logout action.
    """
    session.clear()
    return jsonify({"message": "Logged out successfully"})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

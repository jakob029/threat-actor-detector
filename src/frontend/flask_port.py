"""Flask API for managing user sessions, prompts, and interactions with an LLM backend."""

from flask import Flask, request, jsonify, render_template, session
import requests

# Initialize the Flask app
app = Flask(__name__)

# Define a single base URL for all API requests
BASE_URL = "http://100.77.88.40:5000"
HOST = "10.20.0.20"

# Key for session management
app.secret_key = "Jeppecool1"


@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    """Handle cookie consent acceptance."""
    session["cookies_accepted"] = True
    return jsonify({"message": "Cookies accepted"})


@app.route("/")
def homepage():
    """Render the homepage."""
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
    """Render the info page."""
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template("info.html", is_logged_in=is_logged_in, username=session.get("username"))


@app.route("/user/login", methods=["POST"])
def login():
    """Handle user login."""
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
            return jsonify({"message": "success"})

        return jsonify({"message": response_data.get("message")})
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})


@app.route("/user/register", methods=["POST"])
def register():
    """Handle user registration."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        response = requests.post(f"{BASE_URL}/user/register", json={"username": username, "password": password})
        return jsonify(response.json())
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})


@app.route("/conversations", methods=["POST"])
def conversation():
    """Create a conversation and store the conversation ID (cid) in the session."""
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    try:
        # Match the curl request exactly
        payload = {"uid": uid, "title": "hejsan"}

        # Send request to backend
        response = requests.post(f"{BASE_URL}/conversations", json=payload)
        response_data = response.json()

        if "conversation_id" in response_data:
            # Store CID in the session
            session["cid"] = response_data["conversation_id"]
            session.modified = True  # Ensure session updates persist
            return jsonify({"message": "Conversation created", "cid": session["cid"]})

        # Handle case where 'conversation_id' is missing
        return jsonify({"message": response_data.get("message", "Failed to create conversation")}), 400

    except Exception as e:
        return jsonify({"message": f"Internal server error: {str(e)}"}), 500


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze a prompt using the LLM backend."""
    # Retrieve CID from session
    cid = session.get("cid")

    # Check if CID exists
    if not cid:
        return jsonify({"response": "No conversation ID found. Start a conversation first."}), 400

    # Retrieve prompt from request
    prompt = request.form.get("prompt")

    # Check if prompt is provided
    if not prompt:
        return jsonify({"response": "No prompt received"}), 400

    # Prepare payload for backend request
    analyze_url = f"{BASE_URL}/analyzis"
    payload = {"prompt": prompt, "cid": cid}

    try:
        # Send request to backend
        response = requests.post(analyze_url, json=payload)
        response_data = response.json()

        # Return response to client
        return jsonify(
            {
                "response": response_data.get("response", "No result"),
                "data_points": response_data.get("data_points", {}),
            }
        )
    except requests.RequestException as err:
        return jsonify({"response": f"Error communicating with the server: {str(err)}"}), 500
    except ValueError:
        return jsonify({"response": "Error decoding JSON response from backend"}), 500


@app.route("/logout", methods=["POST"])
def logout():
    """Log out the current user."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host=HOST)

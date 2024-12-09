"""Flask API for managing user sessions, prompts, and interactions with an LLM backend."""

from flask import Flask, request, jsonify, render_template, session
import requests

app = Flask(__name__)

BASE_URL = "http://100.77.88.40:5000"
app.secret_key = "Jeppecool1"

@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    session["cookies_accepted"] = True
    return jsonify({"message": "Cookies accepted"})

@app.route("/")
def homepage():
    cookies_accepted = session.get("cookies_accepted", False)
    is_logged_in = "uid" in session
    return render_template(
        "homepage.html",
        is_logged_in=is_logged_in,
        username=session.get("username"),
        cookies_accepted=cookies_accepted,
    )

@app.route("/info.html")
def info_page():
    is_logged_in = "uid" in session
    return render_template("info.html", is_logged_in=is_logged_in, username=session.get("username"))

@app.route("/user/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        response = requests.post(f"{BASE_URL}/user/login", json={"username": username, "password": password})
        response_data = response.json()
        if response_data.get("message") == "success":
            session.clear()
            session["uid"] = response_data.get("uid")
            session["username"] = username
            return jsonify({"message": "success"})
        return jsonify({"message": response_data.get("message")})
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})

@app.route("/user/register", methods=["POST"])
def register():
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
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    try:
        payload = {"uid": uid, "title": "hejsan"}
        response = requests.post(f"{BASE_URL}/conversations", json=payload)
        response_data = response.json()

        # Check for 'conversation_id' since previously that worked
        if "conversation_id" in response_data:
            session["cid"] = response_data["conversation_id"]
            session.modified = True
            return jsonify({"message": "Conversation created", "cid": session["cid"]})
        
        return jsonify({"message": response_data.get("message", "Failed to create conversation")}), 400
    except Exception as e:
        return jsonify({"message": f"Internal server error: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle sending a prompt to the backend, either starting a new conversation
    or appending a message to an existing one.
    """
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"message": "No prompt provided"}), 400

    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    cid = session.get("cid")  # Get the current conversation ID from the session

    # If there is no active conversation, create one and treat this as a new conversation
    if not cid:
        try:
            # Create a new conversation
            response = requests.post(f"{BASE_URL}/conversations", json={"uid": uid, "title": "Chat Session"})
            response_data = response.json()
            if response.status_code == 200 and "conversation_id" in response_data:
                cid = response_data["conversation_id"]
                session["cid"] = cid  # Store the new conversation ID in the session
                session.modified = True
            else:
                return jsonify({"message": response_data.get("message", "Failed to start conversation")}), 500
        except requests.RequestException as e:
            return jsonify({"message": f"Error starting conversation: {str(e)}"}), 500

        # Now send the first prompt to /analyzis
        try:
            response = requests.post(f"{BASE_URL}/analyzis", json={"prompt": prompt, "cid": cid})
            response_data = response.json()
            if response.status_code == 200:
                # Include data_points for initial analysis
                return jsonify({
                    "message": "success",
                    "response": response_data.get("response"),
                    "data_points": response_data.get("data_points", {})
                })
            else:
                return jsonify({"message": response_data.get("message", "Failed to process prompt")}), 500
        except requests.RequestException as e:
            return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500

    # If a conversation exists, treat this as a follow-up message
    try:
        response = requests.post(f"{BASE_URL}/messages", json={"cid": cid, "text": prompt})
        response_data = response.json()
        if response.status_code == 200 and response_data.get("message") == "success":
            # Return response for follow-up messages
            return jsonify({
                "message": "success",
                "response": response_data.get("response", "No follow-up response")
            })
        else:
            return jsonify({"message": response_data.get("message", "Failed to process follow-up prompt")}), 500
    except requests.RequestException as e:
        return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500



@app.route("/active_conversation", methods=["POST"])
def set_active_conversation():
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    data = request.json
    cid = data.get("cid")

    # If cid is null, clear it from the session
    if cid is None:
        session.pop("cid", None)  # Remove cid from session if it exists
        session.modified = True
        return jsonify({"message": "Active conversation cleared"})

    session["cid"] = cid
    session.modified = True
    return jsonify({"message": "Active conversation updated", "cid": cid})


@app.route("/analyze", methods=["POST"])
def analyze():
    cid = session.get("cid")
    if not cid:
        return jsonify({"response": "No conversation ID found. Start a conversation first."}), 400

    prompt = request.form.get("prompt")
    if not prompt:
        return jsonify({"response": "No prompt received"}), 400

    analyze_url = f"{BASE_URL}/analyzis"
    payload = {"prompt": prompt, "cid": cid}
    try:
        response = requests.post(analyze_url, json=payload)
        response_data = response.json()
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
    session.clear()
    return jsonify({"message": "Logged out successfully"})

if __name__ == "__main__":
    # Run with default host and port
    app.run(debug=True, host="127.0.0.1")

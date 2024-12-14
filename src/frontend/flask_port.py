"""Flask API for managing user sessions, prompts, and interactions with an LLM backend."""

from flask import Flask, request, jsonify, render_template, session
import requests
from datetime import datetime

app = Flask(__name__)

BASE_URL = "http://100.77.88.40:5000"
app.secret_key = "Jeppecool1"


@app.route("/")
def homepage():
    """Render the homepage and sets uid if signed in."""
    cookies_accepted = session.get("cookies_accepted", False)
    is_logged_in = "uid" in session
    uid = session["uid"] if is_logged_in else None  # Assign uid if the user is logged in
    return render_template(
        "homepage.html",
        is_logged_in=is_logged_in,
        username=session.get("username"),
        cookies_accepted=cookies_accepted,
        uid=uid,  # Pass uid to the template
    )


@app.route("/info.html")
def info_page():
    """Route to info page."""
    print(f"Session on info page: {session}")  # Debug log
    is_logged_in = "uid" in session  # Check if the user is logged in
    return render_template("info.html", is_logged_in=is_logged_in, username=session.get("username"))


@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    """Route to keep track if user has accepted cookies."""
    session["cookies_accepted"] = True
    return jsonify({"message": "Cookies accepted"})


@app.route("/user/login", methods=["POST"])
def login():
    """Handle user sign in process."""
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
    """Route to handle user registration."""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        response = requests.post(f"{BASE_URL}/user/register", json={"username": username, "password": password})
        return jsonify(response.json())
    except requests.RequestException as err:
        return jsonify({"message": f"Error communicating with the server: {str(err)}"})


@app.route("/conversations", methods=["POST"])
def create_conversation():
    """Route to create conversations."""
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    try:
        title = datetime.now().strftime("%Y-%m-%d")
        payload = {"uid": uid, "title": title}
        response = requests.post(f"{BASE_URL}/conversations", json=payload)
        response_data = response.json()

        if "conversation_id" in response_data:
            session["cid"] = response_data["conversation_id"]
            session.modified = True
            return jsonify({"message": "Conversation created", "cid": session["cid"]})

        return jsonify({"message": response_data.get("message", "Failed to create conversation")}), 400
    except Exception as e:
        return jsonify({"message": f"Internal server error: {str(e)}"}), 500


@app.route("/conversations", methods=["GET"])
def get_history():
    """Route to retrieve user chat history."""
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401  # Consistent error handling

    print(f"Fetching history for UID: {uid}")  # Debug UID

    try:
        # Forward the request to the backend API
        response = requests.get(f"{BASE_URL}/conversations/{uid}")
        response_data = response.json()

        if response.status_code == 200 and response_data.get("message") == "success":
            # Consistent key for the client
            return jsonify({"message": "success", "conversations": response_data.get("conversations", {})})
        else:
            return (
                jsonify({"message": response_data.get("message", "Failed to fetch conversations")}),
                response.status_code,
            )
    except requests.RequestException as e:
        return jsonify({"message": f"Error communicating with the backend: {str(e)}"}), 500


@app.route("/active_conversation", methods=["POST"])
def set_active_conversation():
    """Set the active conversation and handle cid and uid."""
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    data = request.json
    cid = data.get("cid")

    if cid is None:
        print(f"Clearing active conversation for uid: {uid}")
        session.pop("cid", None)
    else:
        print(f"Setting active conversation to: {cid} for uid: {uid}")
        session["cid"] = cid

    session.modified = True
    return jsonify({"message": "Active conversation updated", "cid": session.get("cid")})


@app.route("/chat", methods=["POST"])
def chat():
    """Start a new conversation or appending a message to an existing one."""
    prompt = request.json.get("prompt")
    is_new = request.json.get("is_new", False)  # Indicate if it's a new conversation
    if not prompt:
        return jsonify({"message": "No prompt provided"}), 400

    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    cid = session.get("cid")

    if not cid and not is_new:
        return jsonify({"message": "No active conversation"}), 400

    if is_new:
        # Use `/analyzis` for the first prompt
        try:
            response = requests.post(f"{BASE_URL}/analyzis", json={"prompt": prompt, "cid": cid})
            response_data = response.json()
            if response.status_code == 200:
                # Mark conversation as started
                session["cid"] = response_data.get("cid", cid)
                session.modified = True
                return jsonify(
                    {
                        "message": "success",
                        "response": response_data.get("response"),
                        "data_points": response_data.get("data_points", {}),
                    }
                )
            else:
                return jsonify({"message": response_data.get("message", "Failed to process first prompt")}), 500
        except requests.RequestException as e:
            return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500

    # Handle follow-up messages
    try:
        response = requests.post(f"{BASE_URL}/messages", json={"cid": cid, "text": prompt})
        response_data = response.json()
        if response.status_code == 200:
            return jsonify({"message": "success", "response": response_data.get("response")})
        else:
            return jsonify({"message": response_data.get("message", "Failed to process follow-up message")}), 500
    except requests.RequestException as e:
        return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500


@app.route("/messages/<cid>", methods=["GET"])
def get_messages(cid):
    """Get messages from a conversation."""
    try:
        response = requests.get(f"{BASE_URL}/messages/{cid}")
        response_data = response.json()

        if response.status_code == 200 and response_data.get("message") == "success":
            return jsonify(
                {
                    "message": "success",
                    "conversation_history": response_data.get("conversation_history"),
                    "data_points": response_data.get("data_points", {}),
                }
            )
        else:
            return jsonify({"message": response_data.get("message", "Failed to fetch messages")}), 500
    except requests.RequestException as e:
        return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500


@app.route("/conversations", methods=["DELETE"])
def delete_all_conversations():
    """Deletes all conversations for the current user (uid)."""
    uid = session.get("uid")
    if not uid:
        return jsonify({"message": "User not logged in"}), 401

    try:
        # Forward the delete request to the backend API with UID in the payload
        payload = {"uid": uid}
        response = requests.delete(f"{BASE_URL}/conversations", json=payload)  # Payload sent as JSON
        if response.status_code == 200:
            return jsonify({"message": "All conversations deleted successfully"})
        else:
            response_data = response.json()
            return (
                jsonify({"message": response_data.get("mesage", "Failed to delete conversations")}),
                response.status_code,
            )
    except requests.RequestException as e:
        return jsonify({"message": f"Error communicating with backend: {str(e)}"}), 500


@app.route("/logout", methods=["POST"])
def logout():
    """Log out user and clear session."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")

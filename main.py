import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ Allow your Firebase domains
CORS(app, origins=[
    "http://localhost:5173",
    "https://bankingstamenetanalysis.firebaseapp.com",
    "https://bankingstamenetanalysis.web.app",
])

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


def send_email(to, subject, html_body, reply_to=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Bank Analyzer Bot <{GMAIL_USER}>"
    msg["To"] = to
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())


# ─── Feedback Route ───────────────────────────────────────────
@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    feedback_text = data.get("feedback")
    timestamp = data.get("timestamp")

    if not all([name, email, feedback_text]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        send_email(
            to=GMAIL_USER,
            subject="New User Feedback - Bank Statement Analyzer",
            reply_to=email,
            html_body=f"""
            <div style="font-family: sans-serif; max-width: 600px;">
                <h2 style="color: #0a2640;">📬 New User Feedback</h2>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> <a href="mailto:{email}">{email}</a></p>
                <p><b>Time:</b> {timestamp}</p>
                <p><b>Feedback:</b></p>
                <div style="background:#f3f4f6; padding:16px; border-radius:8px;">{feedback_text}</div>
                <p style="color:#999; font-size:12px;">Hit Reply to respond directly to the user.</p>
            </div>
            """
        )
        return jsonify({"success": True})
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        return jsonify({"error": "Failed to send feedback."}), 500


# ─── Contact Route ────────────────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    timestamp = data.get("timestamp")

    if not all([name, email, message]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        send_email(
            to=GMAIL_USER,
            subject="New Contact Request - Bank Statement Analyzer",
            reply_to=email,
            html_body=f"""
            <div style="font-family: sans-serif; max-width: 600px;">
                <h2 style="color: #0a2640;">📩 New Contact Request</h2>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> <a href="mailto:{email}">{email}</a></p>
                <p><b>Time:</b> {timestamp}</p>
                <p><b>Message:</b></p>
                <div style="background:#f3f4f6; padding:16px; border-radius:8px;">{message}</div>
            </div>
            """
        )
        return jsonify({"success": True})
    except Exception as e:
        print(f"❌ Contact error: {e}")
        return jsonify({"error": "Failed to send message."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


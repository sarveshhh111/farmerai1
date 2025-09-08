from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

# Hugging Face API info (set as Render environment variable)
HF_API_KEY = os.environ.get("HF_API_KEY")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/sarveshhh111/your-chatbot"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body')

    # Send farmer’s message to Hugging Face model
    response = requests.post(
        HF_MODEL_URL,
        headers=headers,
        json={"inputs": incoming_msg}
    )

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            bot_reply = data[0]["generated_text"]
        elif "generated_text" in data:
            bot_reply = data["generated_text"]
        else:
            bot_reply = str(data)
    else:
        bot_reply = "⚠️ Sorry, I could not fetch a reply from the AI advisory system."

    # Send back SMS via Twilio
    twilio_resp = MessagingResponse()
    twilio_resp.message(bot_reply)
    return str(twilio_resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

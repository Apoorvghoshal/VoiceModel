#///// Code for dial 1,2,3 basic message//////

# from flask import Flask, request, Response

# app = Flask(__name__)

# @app.route("/voice", methods=['POST'])
# def voice():
#     # Step 1: First response with menu options
#     twiml = """
#     <Response>
#         <Gather numDigits="1" action="/gather" method="POST">
#             <Say>Welcome! Press 1 to hear Hi. Press 2 for Good Morning. Press 3 for Good Night.</Say>
#         </Gather>
#         <Say>No input received. Goodbye!</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype='text/xml')

# @app.route("/gather", methods=['POST'])
# def gather():
#     digit = request.form.get('Digits')

#     if digit == "1":
#         message = "Hi!"
#     elif digit == "2":
#         message = "Good Morning!"
#     elif digit == "3":
#         message = "Good Night!"
#     else:
#         message = "Invalid choice. Please try again."

#     twiml = f"""
#     <Response>
#         <Say>{message}</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype='text/xml')


# if __name__ == "__main__":
#     app.run(debug=True)

#////// code to take input from the user/////

# from flask import Flask, request, Response

# app = Flask(__name__)

# @app.route("/voice", methods=['POST'])
# def voice():
#     # Ask the user to speak instead of pressing digits
#     twiml = """
#     <Response>
#         <Gather input="speech" action="/gather" method="POST" timeout="5">
#             <Say>Welcome! Please say Hi, Good Morning, or Good Night.</Say>
#         </Gather>
#         <Say>Sorry, I didn't catch that. Goodbye!</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype='text/xml')

# @app.route("/gather", methods=['POST'])
# def gather():
#     speech = request.form.get('SpeechResult', '').lower()

#     if "hi" in speech:
#         message = "Hi there!"
#     elif "morning" in speech:
#         message = "Good Morning!"
#     elif "night" in speech:
#         message = "Good Night!"
#     else:
#         message = "Sorry, I didn’t understand that."

#     twiml = f"""
#     <Response>
#         <Say>{message}</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype='text/xml')


# if __name__ == "__main__":
#     app.run(debug=True)

#////////// Code to connect model with voice input ///////////////

import os
import requests
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/voice", methods=["POST"])
def voice():
    user_text = request.form.get("SpeechResult", "Hello")
    ai_response = query({"inputs": user_text})

    bot_reply = ai_response[0]["generated_text"] if isinstance(ai_response, list) else "I couldn't process that."

    resp = VoiceResponse()
    resp.say(bot_reply, voice="alice")
    return Response(str(resp), mimetype="application/xml")



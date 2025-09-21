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

# from flask import Flask, request, Response
# import os, requests

# app = Flask(__name__)

# @app.route("/voice", methods=['POST'])
# def voice():
#     # Ask caller for speech input
#     twiml = """
#     <Response>
#         <Gather input="speech" action="/gather" method="POST" timeout="5">
#             <Say>Hello! Please say something after the beep.</Say>
#         </Gather>
#         <Say>No speech detected. Goodbye!</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype='text/xml')


# @app.route("/gather", methods=['POST'])
# def gather():
#     speech = request.form.get("SpeechResult", "")
#     print("Recognized Speech:", speech)  # log to Render

#     # Default fallback
#     message = "Sorry, I couldn't process that."

#     # Get Hugging Face token
#     hf_token = os.getenv("HF_TOKEN")
#     if speech and hf_token:
#         try:
#             headers = {"Authorization": f"Bearer {hf_token}"}
#             data = {"inputs": f"User said: {speech}. Reply politely."}

#             # Send to Hugging Face API
#             r = requests.post(
#                 "https://huggingface.co/facebook/blenderbot-400M-distill",
#                 headers=headers,
#                 json=data,
#                 timeout=10  # don't let it hang too long
#             )

#             print("HF status:", r.status_code)
#             print("HF response:", r.text[:200])  # log first 200 chars

#             if r.status_code == 200:
#                 output = r.json()
#                 if isinstance(output, list) and "generated_text" in output[0]:
#                     message = output[0]["generated_text"]

#         except Exception as e:
#             print("HF API error:", e)

#     # Respond back to Twilio
#     twiml = f"""
#     <Response>
#         <Say>{message}</Say>
#     </Response>
#     """
#     return Response(twiml, mimetype="text/xml")


# if __name__ == "__main__":
#     # Render expects service to bind to 0.0.0.0 and PORT env
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port, debug=True)

#//////// small chat model////////////////

from flask import Flask, request, Response
import os, requests

app = Flask(__name__)

# Hugging Face 90M model endpoint
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-90M"
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(user_text):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    data = {"inputs": user_text}

    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=15)
        r.raise_for_status()
        output = r.json()
        # Hugging Face hosted API returns [{'generated_text': '...'}]
        return output[0]['generated_text']
    except Exception as e:
        print("HF API error:", e)
        return "Sorry, I couldn't process that."

@app.route("/voice", methods=['POST'])
def voice():
    # Ask caller to speak
    twiml = """
    <Response>
        <Gather input="speech" action="/gather" method="POST" timeout="5">
            <Say>Hello! Please say something after the beep.</Say>
        </Gather>
        <Say>No speech detected. Goodbye!</Say>
    </Response>
    """
    return Response(twiml, mimetype='text/xml')

@app.route("/gather", methods=['POST'])
def gather():
    speech = request.form.get("SpeechResult", "")
    print("Recognized Speech:", speech)

    if speech:
        message = query_hf(speech)  # get AI reply
    else:
        message = "I didn't catch that. Please try again."

    twiml = f"""
    <Response>
        <Say>{message}</Say>
    </Response>
    """
    return Response(twiml, mimetype="text/xml")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)



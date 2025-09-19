from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    # Step 1: First response with menu options
    twiml = """
    <Response>
        <Gather numDigits="1" action="/gather" method="POST">
            <Say>Welcome! Press 1 to hear Hi. Press 2 for Good Morning. Press 3 for Good Night.</Say>
        </Gather>
        <Say>No input received. Goodbye!</Say>
    </Response>
    """
    return Response(twiml, mimetype='text/xml')

@app.route("/gather", methods=['POST'])
def gather():
    digit = request.form.get('Digits')

    if digit == "1":
        message = "Hi!"
    elif digit == "2":
        message = "Good Morning!"
    elif digit == "3":
        message = "Good Night!"
    else:
        message = "Invalid choice. Please try again."

    twiml = f"""
    <Response>
        <Say>{message}</Say>
    </Response>
    """
    return Response(twiml, mimetype='text/xml')


if __name__ == "__main__":
    app.run(debug=True)

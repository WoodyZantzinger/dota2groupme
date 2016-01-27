from flask import Flask, request

app = Flask(__name__)

@app.route('/do-test', methods=['POST'])
def git_event():
    result = request.get_json(force=True)
    print("received event" + repr(result))
    return "ACK"

PORT = 5001
TARGET_PORT = 5000

app.run(port=PORT)


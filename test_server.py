from flask import Flask, request
from multiprocessing import Pool

app = Flask(__name__)

@app.route('/results', methods=['POST'])
def git_event():
    result = request.get_json(force=True)
    print("received event" + repr(result))
    return "ACK"

PORT = 5001

p = Pool(5)
p


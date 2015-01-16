import os
from flask import Flask, request

app = Flask(__name__)
#
# https://api.groupme.com/v3/bots/post

@app.route('/message/', methods=['POST'])
def message():
	text=request.form['text']
	print "New Message: " + text
	return text

@app.route("/")
def hello():
	return "Hello world!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
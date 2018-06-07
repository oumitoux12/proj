import os
import sys
import json

import logging
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS


from serve import get_model_api



 # needed for cross-domain requests, allow everything by default
model_api = get_model_api()
app = Flask(__name__)
#CORS(app)
# Tokens from the Facebook page web hooks
ACCESS_TOKEN = "EAAcEEk1InQoBAB9okzEBpGBHSC5hbRxZBKc3K8YbJPZByZBg88qIlnJHcJF9rkR0jv8lmUWA6hKnZC26lZAJ0gPwuXCxvMz2SQZC2WXV1q8uzmE1bWxVKunBzdVZAKGDHkXBRpR9eWZCdNAFdZA5OO1Ugs8nRn7TFDVqOJlCRfOZCzCWgmz8apQ5el"
VERIFY_TOKEN = "secret"

@app.route('/', methods=['GET'])
def verify():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    # Post request using the Facebook Graph API v3.0
    resp = requests.post("https://graph.facebook.com/v3.0/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
    
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    try:
        if(data['entry'][0]['messaging'][0]['message']['text'] != None ):
            message = data['entry'][0]['messaging'][0]['message']['text']
            m=predict(message)
            reply(sender , m)
    except:
        print ("Unexpected error:")
        reply(sender, "")
        return "ok"
        raise
    return "ok"


# load the model


def predict(incoming_msg):
    return model_api(incoming_msg)





if __name__ == '__main__':
    # This is used when running locally.
    app.run(debug=True)
    #app.run(host='127.0.0.1', debug=True)

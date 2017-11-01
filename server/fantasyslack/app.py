import collections
import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/')  
def index():  
    return "Hello, world (and cats)!", 200


@app.route('/api/v1/slack-event', methods=['POST'])
def slack_event():
    if request.json['type'] == 'url_verification':
        if request.json['token'] != config.slack_token:
            return 'Forbidden', 403

        return {
            'challenge': request.json['challenge'], 
        }, 200


try:
    from fantasyslack.secrets import secrets
except:
    secrets = {}

config = collections.ChainMap(os.environ, secrets)


if __name__ == '__main__':
    app.run()

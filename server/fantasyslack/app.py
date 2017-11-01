import collections
import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')  
def index():  
    return "Hello, world (and cats)!", 200


@app.route('/api/v1/slack-event', methods=['POST'])
def slack_event():
    if request.json['type'] == 'url_verification':
        if request.json['token'] != config['slack_token']:
            return 'Forbidden', 403

        return jsonify({
            'challenge': request.json['challenge'], 
        })


try:
    s3_client = boto3.client('s3')
    response = s3_client.get_object(
        Bucket='fantasyslack-conf',
        Key='secrets.json',
    )
    remote_secrets = json.load(response['Body'].read())
except:
    remote_secrets = {}

try:
    with open('secrets.json') as secrets_file:
        local_secrets = json.load(secrets_file)
except:
    local_secrets = {}

config = collections.ChainMap(os.environ, remote_secrets, local_secrets)


if __name__ == '__main__':
    app.run()

import boto3
import collections
import datetime
import json
import operator
import os
import pprint

import jose.jwt
import requests

from flask import Flask, request, jsonify, abort
import fantasyslack.models


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return "Hello, world (and cats)!", 200


@app.route('/api/v1/slack-event', methods=['POST'])
def slack_event():
    RESPONSE_OK = jsonify({
        'response': 'ok'
    })

    RESPONSE_FORBIDDEN = jsonify({
        'response': 'forbidden'
    })

    if request.json['type'] == 'url_verification':
        if request.json['token'] != config['slack_token']:
            return RESPONSE_FORBIDDEN, 403

        return jsonify({
            'challenge': request.json['challenge'],
        })
    else:
        if request.json['token'] != config['slack_token']:
            return RESPONSE_FORBIDDEN, 403

        del request.json['token']

        event = fantasyslack.models.EventModel(from_slack=request.json)
        event.save()

        return RESPONSE_OK


def verify_identity():
    pool_id = 'us-east-1_APXGoWFHh'
    region = 'us-east-1'
    response = requests.get(f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json")

    keys = {
        key['kid']: key
        for key in response.json().get('keys', [])
    }

    token = request.headers['accessToken']

    try:
        header = jose.jwt.get_unverified_header(token)
    except jose.exceptions.JWTError:
        abort(403)

    key = keys[header['kid']]

    try:
        contents = jose.jwt.decode(token, key)
    except jose.ExpiredSignatureError:
        abort(403)

    if contents['iss'] != 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_APXGoWFHh':
        abort(403)

    if contents['token_use'] != 'access':
        abort(403)


@app.route('/api/v1/game/<slug>/players', methods=['GET'])
def players(slug):
    verify_identity()

    # TODO: Need to use slug to get a Slack workspace to look at

    start = datetime.datetime(2017, 10, 1)
    end = datetime.datetime(2017, 11, 1)

    players = collections.defaultdict(lambda: collections.defaultdict(int))

    for player_point in fantasyslack.models.PlayerPointModel.scan(fantasyslack.models.PlayerPointModel.created.between(start, end)):
        players[player_point.player.name][player_point.category.name] += 1

    table = [
        {
            'name': player_name,
            'points': sum(entry.values()),
        }
        for player_name, entry in players.items()
    ]

    for idx, row in enumerate(sorted(table, key=operator.itemgetter('points'), reverse=True)):
        row['rank'] = idx+1

    return jsonify(table)


def get_config():
    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(
            Bucket='fantasyslack-conf',
            Key='secrets.json',
        )

        remote_secrets = json.load(response['Body'])
    except Exception as e:
        print("Could not load remote secrets:", e)
        remote_secrets = {}

    try:
        with open('secrets.json') as secrets_file:
            local_secrets = json.load(secrets_file)
    except Exception as e:
        print("Could not load local secrets:", e)
        local_secrets = {}

    return collections.ChainMap(os.environ, remote_secrets, local_secrets)


config = get_config()


if __name__ == '__main__':
    app.run()

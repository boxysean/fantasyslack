import boto3
import collections
import datetime
import dateutil
import json
import logging
import operator
import os
import pprint

from flask import Flask, request, jsonify, abort

import fantasyslack.auth
import fantasyslack.models
import fantasyslack.util


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


@app.route('/api/v1/games/<slug>/players', methods=['GET'])
@fantasyslack.auth.login_required
def players(slug, user_email=None):
    game = fantasyslack.util.get_game_by_slug(slug)

    if not game:
        abort(404)

    user = fantasyslack.util.get_user_by_email(user_email)

    if not user:
        abort(403)

    team = fantasyslack.util.get_game_team_by_user_id(game.id, user.id)

    if not team:
        abort(403)

    start_raw = request.args.get('start', None)
    end_raw = request.args.get('end', None)

    if start_raw:
        start = dateutil.parser.parse(start_raw)
    else:
        start = datetime.datetime(2017, 10, 1)

    if end_raw:
        end = dateutil.parser.parse(end_raw)
    else:
        end = datetime.datetime(2017, 11, 1)

    player_records = {}

    class PlayerRecord:
        def __init__(self, name, team):
            self.name = name
            self.team = team
            self.points = collections.defaultdict(int)

    # Prepopulate all known players

    existing_players = fantasyslack.models.PlayerModel.scan(
        (fantasyslack.models.PlayerModel.slack_team_id == game.slack_team_id) &\
        (fantasyslack.models.PlayerModel.game_id == game.id)
    )

    for player in existing_players:
        player_records[player.id] = PlayerRecord(player.name, player.current_team.name)

    # Then go through the accumulated points and sum them

    for player_point in fantasyslack.models.PlayerPointModel.scan(
            fantasyslack.models.PlayerPointModel.created.between(start, end) &\
            (fantasyslack.models.PlayerPointModel.game_id == game.id)
        ):
        if player_point.player_id not in player_records:
            player_records[player_point.player_id] = PlayerRecord(player.name, player.current_team.name)
        player_records[player_point.player_id].points[player_point.category.name] += 1

    # Also grab their draft orders for this user

    draft_order = {
        d.attribute_values['player_id']: d.attribute_values['order']
        for d in fantasyslack.models.DraftSelectionModel.scan(
            (fantasyslack.models.DraftSelectionModel.game_id == game.id) &\
            (fantasyslack.models.DraftSelectionModel.team_id == team.id)
        )
    }

    table = [
        {
            'name': player_record.name,
            'points': sum(player_record.points.values()),
            'team': player_record.team,
            'draftOrder': draft_order.get(player_id, None),
        }
        for player_id, player_record in player_records.items()
    ]

    for idx, row in enumerate(sorted(table, key=operator.itemgetter('points'), reverse=True), 1):
        row['rank'] = idx

    return jsonify({
        'players': table,
        'start': start.isoformat(),
        'end': end.isoformat(),
    })


@app.route('/api/v1/games', methods=['GET'])
def list_games():
    def expand(obj):
        if type(obj) == dict:
            return {
                k: expand(v)
                for k, v in obj.items()
            }
        elif type(obj) == fantasyslack.models.GameDraftAttribute:
            return expand(obj.attribute_values)
        else:
            return obj

    return jsonify([
        expand(game.attribute_values)
        for game in fantasyslack.models.GameModel.scan()
    ])


@app.route('/api/v1/games/<slug>', methods=['GET'])
def get_game(slug):
    game = fantasyslack.util.get_game_by_slug(slug)

    if not game:
        abort(404)

    return jsonify({
        'name': game.attribute_values['name'],
        'slug': slug,
        'start': game.attribute_values['start'].isoformat(),
        'end': game.attribute_values['end'].isoformat(),
        'categories': [category.name for category in game.categories],
        'teams': [team.name for team in game.teams],
        'categories': fantasyslack.util.score_categories(game),
        'standings': fantasyslack.util.score_game(game),
        'draft': game.attribute_values['draft'].attribute_values,
        'admins': [fantasyslack.util.get_user_by_id(user_id).name
                   for user_id in game.attribute_values['admin_user_ids']],
    })


@app.route('/api/v1/games/<game_slug>/teams/<team_slug>', methods=['PUT'])
@fantasyslack.auth.login_required
def put_game_team(game_slug, team_slug, user_email=None):
    game = fantasyslack.util.get_game_by_slug(game_slug)

    if not game:
        abort(404)

    team = fantasyslack.util.get_game_team_by_slug(game.id, team_slug)

    if not team:
        abort(404)

    user = fantasyslack.util.get_user_by_email(user_email)

    if not user:
        abort(403)

    if team.user_id != user.id:
        abort(403)

    for draft_order_record in request.json['draftOrder']:
        player = fantasyslack.util.get_game_player_by_name(game.id, draft_order_record['player'])

        # Upsert:

        try:
            existing_draft_selection = list(fantasyslack.models.DraftSelectionModel.scan(
                (fantasyslack.models.DraftSelectionModel.game_id == game.id) &\
                (fantasyslack.models.DraftSelectionModel.team_id == team.id) &\
                (fantasyslack.models.DraftSelectionModel.player_id == player.id)
            ))[0]

            if not draft_order_record['order']:
                existing_draft_selection.delete()
            else:
                existing_draft_selection.update({
                    'order': {
                        'value': draft_order_record['order'],
                        'action': 'PUT',
                    },
                })
        except IndexError:
            if draft_order_record['order']:
                fantasyslack.models.DraftSelectionModel(
                    game_id=game.id,
                    team_id=team.id,
                    player_id=player.id,
                    order=draft_order_record['order'],
                ).save()

    return jsonify({
        'response': 'ok'
    })


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

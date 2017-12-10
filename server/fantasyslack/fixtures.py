import collections
import datetime
import itertools
import logging
import random

import pynamodb.exceptions

import fantasyslack.models
import fantasyslack.util


def _make_model(cls, **kwargs):
    obj = cls(**kwargs)
    obj.save()
    return obj


def _clear_fixtures():
    for model_class in fantasyslack.util.model_classes():
        print(f"> Clearing {model_class}")
        try:
            with model_class.batch_write() as batch:
                for item in model_class.scan():
                    batch.delete(item)
        except pynamodb.exceptions.ScanError as e:
            if 'Requested resource not found' in e.msg:
                logging.warn(e.msg)
            else:
                raise e


def create_fixtures(args):
    if args.clear:
        _clear_fixtures()

    if args.do_not_create:
        return

    if args.pre_game:
        game_id = 'FAKE-PRE-GAME-ID'
    else:
        game_id = 'FAKE-GAME-ID'

    slack_team_id = 'T123'

    player_names = [
        'boxysean',
        'Jerry',
        'George',
        'Elaine',
        'Kramer',
        'Newman',
    ]

    players_per_team = 2

    slack_users = [
        _make_model(fantasyslack.models.InternalSlackUserModel,
            name=player_name,
            slack_team_id=slack_team_id,
            slack_user_id=str(hash(player_name)),
        ) for player_name in player_names
    ]

    users = [
        _make_model(fantasyslack.models.UserModel,
            email=f"{player_name.lower()}@gmail.com",
            name=player_name,
            internal_slack_user_ids=[slack_user.id],
            admin=player_name == 'boxysean',
        ) for player_name, slack_user in list(zip(player_names, slack_users))[0:3]
    ]

    admin_user_id = [user.id for user in users if user.email == 'boxysean@gmail.com'][0]

    players = [
        _make_model(fantasyslack.models.PlayerModel,
            game_id=game_id,
            internal_slack_user_id=slack_user.id,
            slack_team_id=slack_team_id,
            name=slack_user.name,
        ) for slack_user in slack_users
    ]

    team_names = [
        'Team Unicorn',
        'Team Donkey',
        'Team Whale',
    ]

    player_ids_iterator = iter([player.id for player in players])

    teams = [
        _make_model(fantasyslack.models.TeamModel,
            game_id=game_id,
            user_id=user.id,
            name=team_name,
            current_player_ids=list(itertools.islice(player_ids_iterator, 0, 2)),
            current_points=[],
        )
        for team_name, user in zip(team_names, users)
    ]

    category_names = [
        'Controversial',
        'Emoji Master',
        'Nite Owl',
    ]

    categories = [
        _make_model(fantasyslack.models.CategoryModel,
            game_id=game_id,
            name=category_name,
        )
        for category_name in category_names
    ]

    if args.pre_game:
        team_order = [team.id for team in teams]
        random.shuffle(team_order)

        draft = {
            'has_started': False,
            'has_ended': False,
            'team_order': team_order,
            'position': 0,
            'start': datetime.datetime(2017, 12, 10, 17, 0, 0),
        }

        game = _make_model(fantasyslack.models.GameModel,
            id=game_id,
            name='Fake Pre-game',
            slug='fake-pre-game',
            team_ids=[team.id for team in teams],
            category_ids=[category.id for category in categories],
            start=datetime.datetime(2018, 1, 1),
            end=datetime.datetime(2018, 2, 1),
            players_per_team=players_per_team,
            draft=draft,
            admin_user_ids=[admin_user_id],
            slack_team_id=slack_team_id,
        )
    else:
        team_order = [team.id for team in teams]
        random.shuffle(team_order)

        draft = {
            'has_started': True,
            'has_ended': True,
            'team_order': team_order,
            'position': players_per_team * len(teams),
            'start': datetime.datetime(2017, 10, 31, 17, 0, 0),
        }

        game = _make_model(fantasyslack.models.GameModel,
            id=game_id,
            name='Fake Game',
            slug='fake-game',
            team_ids=[team.id for team in teams],
            category_ids=[category.id for category in categories],
            start=datetime.datetime(2017, 11, 1),
            end=datetime.datetime(2017, 12, 1),
            players_per_team=players_per_team,
            draft=draft,
            admin_user_ids=[admin_user_id],
            slack_team_id=slack_team_id,
        )

        _generate_player_points(game_id, players, categories, teams)


def _random_datetime(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def _generate_player_points(game_id, players, categories, teams, start=None, end=None):
    if not start:
        start = datetime.datetime(2017, 11, 1)

    if not end:
        end = datetime.datetime(2017, 12, 1)

    player_id_team_map = {
        player_id: team
        for team in teams
        for player_id in team.current_player_ids
    }

    team_points = collections.defaultdict(lambda: 0)

    for player in players:
        team = player_id_team_map[player.id]
        for category in categories:
            points = random.randrange(10)
            for i in range(points):
                event_time = _random_datetime(start, end)
                _make_model(fantasyslack.models.PlayerPointModel,
                    game_id=game_id,
                    created=event_time,
                    updated=event_time,
                    player_id=player.id,
                    category_id=category.id,
                    related_slack_event_ids=[],
                )
            team_points[(team, category.id)] += points

    for (team, category_id), points in team_points.items():
        team.current_points.append({
            'category_id': category_id,
            'points': points,
        })
        team.save()

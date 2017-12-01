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

    slack_users = [
        _make_model(fantasyslack.models.SlackUserModel,
            name=player_name,
            slack_team_id=slack_team_id,
            slack_user_id=str(hash(player_name)),
        ) for player_name in player_names
    ]

    users = [
        _make_model(fantasyslack.models.UserModel,
            email=f"{player_name.lower()}@gmail.com",
            slack_user_id=slack_user.id,
        ) for player_name, slack_user in list(zip(player_names, slack_users))[0:3]
    ]

    players = [
        _make_model(fantasyslack.models.PlayerModel,
            game_id=game_id,
            slack_user_id=slack_user.id,
        ) for slack_user in slack_users
    ]

    managers = [
        _make_model(fantasyslack.models.ManagerModel,
            game_id=game_id,
            player_id=player.id,
            user_id=user.id,
        )
        for player, user in list(zip(players, users))[0:3]
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
            manager_id=manager.id,
            name=team_name,
            current_player_ids=list(itertools.islice(player_ids_iterator, 0, 2)),
            current_points=[],
        )
        for team_name, manager in zip(team_names, managers)
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

    game = _make_model(fantasyslack.models.GameModel,
        id=game_id,
        name='Fake Game',
        slug='fake-game',
        team_ids=[team.id for team in teams],
        category_ids=[category.id for category in categories],
        start=datetime.datetime(2017, 11, 1),
        end=datetime.datetime(2017, 12, 1),
    )

    _generate_player_points(game_id, players, categories, teams)


def _random_datetime(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def _generate_player_points(game_id, players, categories, teams, start=None, end=None):
    if not start:
        start = datetime.datetime(2017, 10, 1)

    if not end:
        end = datetime.datetime(2017, 11, 1)

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
                    related_event_ids=[],
                )
            team_points[(team, category.id)] += points

    for (team, category_id), points in team_points.items():
        team.current_points.append({
            'category_id': category_id,
            'points': points,
        })
        team.save()

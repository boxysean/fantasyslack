import datetime
import random

import fantasyslack.models
import fantasyslack.util


def _make_model(cls, **kwargs):
    obj = cls(**kwargs)
    obj.save()
    return obj


def _clear_fixtures():
    for model_class in fantasyslack.util.model_classes():
        print(f"> Clearing {model_class}")
        with model_class.batch_write() as batch:
            for item in model_class.scan():
                batch.delete(item)


def create_fixtures(args):
    if args.clear:
        _clear_fixtures()

    if args.do_not_create:
        return

    slack_team_id = 'T123'

    player_names = [
        'Jerry',
        'George',
        'Elaine',
        'Kramer',
        'Newman',
    ]

    players = [
        _make_model(fantasyslack.models.PlayerModel,
            slack_team_id=slack_team_id,
            slack_user_id=str(hash(player_name)),
            name=player_name,
        ) for player_name in player_names
    ]

    managers = [
        _make_model(fantasyslack.models.ManagerModel,
            slack_team_id=slack_team_id,
            slack_user_id=player.slack_user_id,
            player_id=player.id,
        )
        for player in players[0:3]
    ]

    team_names = [
        'Team Unicorn',
        'Team Donkey',
        'Team Whale',
    ]

    teams = [
        _make_model(fantasyslack.models.TeamModel,
            manager_id=manager.id,
            name=team_name,
            current_player_ids=[],
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
            name=category_name,
        )
        for category_name in category_names
    ]

    _make_model(fantasyslack.models.GameModel,
        name='Test Game',
        team_ids=[team.id for team in teams],
        category_ids=[category.id for category in categories],
        start=datetime.datetime(2017, 11, 1),
        end=datetime.datetime(2017, 12, 1),
    )

    _generate_player_points(players, categories)


def _random_datetime(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def _generate_player_points(players, categories, start=None, end=None):
    if not start:
        start = datetime.datetime(2017, 10, 1)

    if not end:
        end = datetime.datetime(2017, 11, 1)

    for player in players:
        for category in categories:
            points = random.randrange(10)
            for i in range(points):
                event_time = _random_datetime(start, end)
                _make_model(fantasyslack.models.PlayerPointModel,
                    created=event_time,
                    updated=event_time,
                    player_id=player.id,
                    category_id=category.id,
                    related_event_ids=[],
                )

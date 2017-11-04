import datetime

import fantasyslack.models


def _make_model(cls, **kwargs):
    obj = cls(**kwargs)
    obj.save()
    return obj


def create_fixtures(args):
    slack_team_id = 'T123'

    player_names = [
        'Jerry',
        'George',
        'Elaine',
        'Kramer',
    ]

    players = [
        _make_model(fantasyslack.models.PlayerModel,
            slack_team_id=slack_team_id,
            slack_user_id=str(hash(player_name)),
        ) for player_name in player_names
    ]

    managers = [
        _make_model(fantasyslack.models.ManagerModel,
            slack_team_id=slack_team_id,
            slack_user_id=player.slack_user_id,
            player_id=player.id,
        )
        for player in players[0:2]
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
        for team_name, manager in zip(team_names, managers[0:3])
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

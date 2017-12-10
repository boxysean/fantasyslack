import collections
import math
import operator
import slugify

import fantasyslack.models


def _is_model_class(element):
    try:
        return issubclass(element, fantasyslack.models.BaseModel) and element != fantasyslack.models.BaseModel
    except TypeError:
        return False


def model_classes():
    for entry in dir(fantasyslack.models):
        element = getattr(fantasyslack.models, entry)
        if _is_model_class(element):
            yield element


def get_user_by_email(email):
    try:
        return list(fantasyslack.models.UserModel.scan(
            fantasyslack.models.UserModel.email == email
        ))[0]
    except IndexError:
        return None


def get_user_by_id(user_id):
    try:
        return list(fantasyslack.models.UserModel.query(user_id))[0]
    except IndexError:
        return None


def get_game_by_slug(slug):
    try:
        return list(fantasyslack.models.GameModel.scan(
            fantasyslack.models.GameModel.slug == slug
        ))[0]
    except IndexError:
        return None


def get_game_team_by_slug(game_id, slug):
    for team in fantasyslack.models.TeamModel.scan(fantasyslack.models.TeamModel.game_id == game_id):
        if slugify.slugify(team.name) == slug:
            return team
    else:
        return None


def get_game_team_by_user_id(game_id, user_id):
    try:
        return list(fantasyslack.models.TeamModel.scan(
            (fantasyslack.models.TeamModel.game_id == game_id)
            & (fantasyslack.models.TeamModel.user_id == user_id)
        ))[0]
    except IndexError:
        return None


def get_game_player_by_name(game_id, player_name):
    try:
        return list(fantasyslack.models.PlayerModel.scan(
            (fantasyslack.models.PlayerModel.game_id == game_id)
            & (fantasyslack.models.PlayerModel.name == player_name)
        ))[0]
    except IndexError:
        return None


def score_categories(game):
    """
    Computes the points and scores per team per category.
    """
    class TeamCategoryRecord:
        def __init__(self, name, points, score):
            self.name = name
            self.points = points
            self.score = score

        def __repr__(self):
            return f"({self.name}, {self.points}, {self.score})"

    records = collections.defaultdict(list)

    for category in game.categories:
        for team in game.teams:
            records[category].append(TeamCategoryRecord(
                team.name,
                team.get_category_points(category),
                None,
            ))

        # Sort descending by (points, name).
        records[category] = list(reversed(sorted(records[category], key=operator.attrgetter('points', 'name'))))

        # Give the highest scoring team full points.
        records[category][0].score = len(game.teams)

        # If there's a tie between consecutive teams, ensure that the higher
        # team is knocked down 0.5 (if it hasn't been already) and then give
        # the lower team the same score as the higher team.
        fun_list = reversed(list(enumerate(zip(reversed(records[category][0:-1]), reversed(records[category][1:])), 1)))
        for current_score, (team_up, team_down) in fun_list:
            if team_up.points == team_down.points:
                if team_up.score == math.floor(team_up.score):
                    team_up.score -= 0.5
                team_down.score = team_up.score
            else:
                team_down.score = current_score

    return {
        category.name: [
            {
                'team': record.name,
                'points': record.points,
                'score': record.score,
            }
            for record in records[category]
        ]
        for category in game.categories
    }


def score_game(game):
    class TeamRecord:
        def __init__(self, name, points, score, rank):
            self.name = name
            self.points = points
            self.score = score
            self.rank = rank

        def __repr__(self):
            return f"({self.name}, {self.points}, {self.score}, {self.rank})"

    class keydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            else:
                ret = self[key] = self.default_factory(key)
                return ret

    record_map = keydefaultdict(lambda team_name: TeamRecord(
        team_name, 0, 0, None
    ))

    for category_name, team_category_records in score_categories(game).items():
        for team_category_record in team_category_records:
            team_name = team_category_record['team']
            team_record = record_map[team_name]
            team_record.points += team_category_record['points']
            team_record.score += team_category_record['score']

    # Sort descending by (score, points, name).
    records = sorted(
        record_map.values(),
        key=operator.attrgetter('score', 'points', 'name'),
        reverse=True,
    )

    # Give the first-placed team first place.
    records[0].rank = 1

    # If there's a tie in score and points between consecutive teams, give the
    # lower team the same rank as the higher team.
    fun_list = list(enumerate(zip(records[0:-1], records[1:]), 2))
    for current_rank, (team_up, team_down) in fun_list:
        if team_up.score == team_down.score and team_up.points == team_down.points:
            team_down.rank = team_up.rank
        else:
            team_down.rank = current_rank

    return [
        {
            'team': record.name,
            'points': record.points,
            'score': record.score,
            'rank': record.rank,
        }
        for record in records
    ]

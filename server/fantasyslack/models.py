import datetime
import uuid

from pynamodb.attributes import UTCDateTimeAttribute, ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


_cache = {}

def _from_cache(model, id):
    if id in _cache:
        return _cache[id]
    else:
        res = list(model.query(id))[0]
        _cache[id] = res
        return res


class BaseMeta(object):
    region = 'us-east-1'
    read_capacity_units = 1
    write_capacity_units = 1


class BaseModel(Model):
    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    created = UTCDateTimeAttribute(range_key=True, default=datetime.datetime.utcnow())
    updated = UTCDateTimeAttribute(default=datetime.datetime.utcnow())


class EventModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-events'

    from_slack = MapAttribute()


class ManagerModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-managers'

    slack_team_id = UnicodeAttribute()  # secondary key A
    slack_user_id = UnicodeAttribute()  # secondary key A
    player_id = UnicodeAttribute()


class ScoreHistoryAttribute(MapAttribute):
    category_id = UnicodeAttribute()
    points = NumberAttribute()
    score = NumberAttribute()


class ScoreHistoryModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-scoringhistory'

    """
    The intent of this model is to capture all points of change (no pun
    intended) to look back at key events. Duplicate data, but easy
    lookups.

    Example:

    [
        {  # ScoreHistoryModel
            timestamp: 1234567890,
            team_id: "team123",
            game_id: "game2",
            scoring: [
                {  # ScoreHistoryAttribute
                    "category_id": "cat456",
                    "points": 12,
                    "score": 1.5
                },
                ...
            ]
        },
        ...
    ]

    """
    team_id = UnicodeAttribute()
    game_id = UnicodeAttribute()
    scoring = ListAttribute(of=ScoreHistoryAttribute)


class GameModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-games'

    name = UnicodeAttribute()
    team_ids = ListAttribute()  # probably doesn't change
    category_ids = ListAttribute()  # must not change
    start = UTCDateTimeAttribute()
    end = UTCDateTimeAttribute()


class TeamModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-teams'

    manager_id = UnicodeAttribute()  # secondary key A
    name = UnicodeAttribute()
    current_player_ids = ListAttribute()
    current_points = ListAttribute()


class TransactionMapAttribute(MapAttribute):
    player_id = UnicodeAttribute()
    destination = UnicodeAttribute()  # either a Team ID or "pool" / "dropped"


class TransactionModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-transactions'

    team_id = UnicodeAttribute()
    player_id = UnicodeAttribute()
    action = UnicodeAttribute()  # add, drop, trade, banned(?)
    transactions = ListAttribute(of=TransactionMapAttribute)
    ts = UTCDateTimeAttribute()


class PlayerModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-players'

    slack_team_id = UnicodeAttribute()
    slack_user_id = UnicodeAttribute()
    name = UnicodeAttribute()


class PlayerPointModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-points'

    player_id = UnicodeAttribute()
    category_id = UnicodeAttribute()
    related_event_ids = ListAttribute()

    @property
    def player(self):
        return _from_cache(PlayerModel, self.player_id)

    @property
    def category(self):
        return _from_cache(CategoryModel, self.category_id)


class CategoryModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-categories'

    name = UnicodeAttribute()


class DraftSelectionModel(BaseModel):
    class Meta(BaseMeta):
        table_name = 'fantasyslack-draftselection'

    player_id = UnicodeAttribute()
    team_id = UnicodeAttribute()
    game_id = UnicodeAttribute()
    order = NumberAttribute()

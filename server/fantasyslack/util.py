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


def get_game_by_slug(slug):
    try:
        return list(fantasyslack.models.GameModel.scan(
            fantasyslack.models.GameModel.slug == slug
        ))[0]
    except IndexError:
        return None


def get_game_manager_by_user_id(game_id, user_id):
    try:
        return list(fantasyslack.models.ManagerModel.scan(
            (fantasyslack.models.ManagerModel.game_id == game_id)
            & (fantasyslack.models.ManagerModel.user_id == user_id)
        ))[0]
    except IndexError:
        return None

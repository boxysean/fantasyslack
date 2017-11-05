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



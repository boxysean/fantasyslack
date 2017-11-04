import argparse

import fantasyslack.models


def _is_model_class(element):
    try:
        return issubclass(element, fantasyslack.models.BaseModel) and element != fantasyslack.models.BaseModel
    except TypeError:
        return False


def create_tables(args):
    for entry in dir(fantasyslack.models):
        element = getattr(fantasyslack.models, entry)
        if _is_model_class(element):
            if args.delete:
                print(f"> Deleting {element}")
                element.create_table()
            if not args.do_not_create:
                print(f"> Creating {element}")
                element.create_table()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fantasy Slack CLI')
    subparser = parser.add_subparsers()

    create_table_parser = subparser.add_parser('create_table')
    create_table_parser.add_argument('--delete', action='store_true', default=False)
    create_table_parser.add_argument('--do-not-create', action='store_true', default=False)
    create_table_parser.set_defaults(func=create_tables)

    args = parser.parse_args()
    args.func(args)

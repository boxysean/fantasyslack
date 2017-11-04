import argparse

import fantasyslack.fixtures
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

    create_tables_parser = subparser.add_parser('create_tables')
    create_tables_parser.add_argument('--delete', action='store_true', default=False)
    create_tables_parser.add_argument('--do-not-create', action='store_true', default=False)
    create_tables_parser.set_defaults(func=create_tables)

    create_fixtures_parser = subparser.add_parser('create_fixtures')
    create_fixtures_parser.set_defaults(func=fantasyslack.fixtures.create_fixtures)

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_usage()
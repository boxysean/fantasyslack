import argparse

import fantasyslack.fixtures
import fantasyslack.models
import fantasyslack.util


def create_tables(args):
    for model_class in fantasyslack.util.model_classes():
        if args.delete:
            print(f"> Deleting {model_class}")
            model_class.delete_table()
        if not args.do_not_create:
            print(f"> Creating {model_class}")
            model_class.create_table()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fantasy Slack CLI')
    subparser = parser.add_subparsers()

    create_tables_parser = subparser.add_parser('create_tables')
    create_tables_parser.add_argument('--delete', action='store_true', default=False)
    create_tables_parser.add_argument('--do-not-create', action='store_true', default=False)
    create_tables_parser.set_defaults(func=create_tables)

    create_fixtures_parser = subparser.add_parser('create_fixtures')
    create_fixtures_parser.add_argument('--clear', action='store_true', default=False)
    create_fixtures_parser.add_argument('--do-not-create', action='store_true', default=False)
    create_fixtures_parser.set_defaults(func=fantasyslack.fixtures.create_fixtures)

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_usage()
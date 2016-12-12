#!/usr/bin/env python
# encoding: utf-8

""" A module to manage the app
To dump a database:
    python manage.py dump
To restore a database:
    python manage.py restore dump/161114_071346_zesk06.dump

"""

from __future__ import print_function
import argparse
import logging

import scores.common
import scores.database


def dump(args):
    """dump"""
    if args.uri and len(args.uri) > 0:
        database = scores.database.Database(uri=args.uri)
    else:
        database = scores.database.Database.get_db()
    database.dump()


def restore(args):
    """restore"""
    if args.uri and len(args.uri) > 0:
        database = scores.database.Database(uri=args.uri)
    else:
        database = scores.database.Database.get_db()
    database.restore(delete=args.delete, dump_folder=args.dumpfolder)


def main():
    """Maining."""
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='sub_name', help='sub commands')
    # so you wanna dump
    dump_parser = subparser.add_parser('dump', help='dump the database')
    dump_parser.add_argument('--uri', action='store', help='The database URI to dump')
    dump_parser.set_defaults(func=dump)

    # so you wanna restore
    dump_parser = subparser.add_parser('restore', help='restore the database')
    dump_parser.add_argument('--uri', action='store', help='The database URI to dump')
    dump_parser.add_argument('--delete', action='store_true',
                             help='Delete the database before restoring')
    dump_parser.add_argument('dumpfolder', action='store', help='The dumpfolder to restore')
    dump_parser.set_defaults(func=restore)

    pargs = parser.parse_args()
    pargs.func(pargs)


if __name__ == '__main__':
    main()

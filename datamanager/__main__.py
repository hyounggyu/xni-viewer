import argparse

from .create import start_create
from .view import start_view, start_remoteview

def parse_args():
    parser = argparse.ArgumentParser(prog='datamanager')
    parser.add_argument('--version', help='version help')

    subparsers = parser.add_subparsers(help='sub commands')

    create_parser = subparsers.add_parser('create', help='create help')
    create_parser.add_argument('path', help='path help')
    create_parser.add_argument('-o', '--output', help='output help')
    create_parser.add_argument('-i', '--image-prefix', help='image prefix help')
    create_parser.add_argument('-b', '--background-prefix', help='background image prefix help', required=False)
    create_parser.add_argument('-d', '--dark-prefix', help='dark image prefix help', required=False)
    create_parser.set_defaults(func=start_create)

    rv_parser = subparsers.add_parser('remoteview', help='removeview help')
    rv_parser.add_argument('--ip', help='ip help', required=False)
    rv_parser.add_argument('--port', help='port help', required=False)
    rv_parser.add_argument('--slice', help='slice help default 0:1:1', required=False)
    rv_parser.add_argument('--stop', help='stop help', required=False, action='store_true')
    rv_parser.set_defaults(func=start_remoteview)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

parse_args()

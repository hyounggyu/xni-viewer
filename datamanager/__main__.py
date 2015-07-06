import argparse
from pathlib import Path


def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])

def new_dataset(args):
    from xni.io import dataset
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, p in dataset.create(args.output, images, bgnds, darks):
        print(p)

def remote_view(args):
    import sys
    import zmq
    from PyQt4 import QtGui
    from xni.io import dataset
    from .view import ViewWindow

    dset = dataset.recv()

    app = QtGui.QApplication(sys.argv)
    win = ViewWindow(dset)
    sys.exit(app.exec_())

def run_qt():
    import sys
    from .gui import App
    app = App(sys.argv)
    sys.exit(app.exec_())

def parse_args():
    parser = argparse.ArgumentParser(prog='datamanager')
    parser.add_argument('--version', help='version help')

    subparsers = parser.add_subparsers(help='sub commands')

    new_parser = subparsers.add_parser('new', help='new help')
    new_parser.add_argument('path', help='path help')
    new_parser.add_argument('-o', '--output', help='output help')
    new_parser.add_argument('-i', '--image-prefix', help='image prefix help')
    new_parser.add_argument('-b', '--background-prefix', help='background image prefix help', required=False)
    new_parser.add_argument('-d', '--dark-prefix', help='dark image prefix help', required=False)
    new_parser.set_defaults(func=new_dataset)

    rv_parser = subparsers.add_parser('remoteview', help='removeview help')
    rv_parser.set_defaults(func=remote_view)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        run_qt()

parse_args()
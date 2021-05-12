import os
import argparse

from core import engine
from core import utils

parser = argparse.ArgumentParser("Test RL build")
parser.add_argument("src", help="Path to build data")
parser.add_argument("dst", help="PDF to generate", nargs="?")
args = parser.parse_args()

srcDir = os.path.dirname(os.path.abspath(args.src))
dst = args.dst if args.dst is not None else "document.pdf"

e = engine.Engine()
data = utils.loadFile(args.src)
build = e.processBlocks(data, srcDir)
e.build(build, dst)

#!/usr/bin/env python3
import argparse
from pathlib import Path
import interpreter, parser

arg_parser = argparse.ArgumentParser(description = "simple cli for dih")

arg_parser.add_argument("file", nargs = "?", help = "dih code file to run", type = Path)
arg_parser.add_argument("-c", "--command", help = "dih code text to run")

args = arg_parser.parse_args()

if (args.file is None) == (args.command is None):
    arg_parser.error("provide exactly one thing to do!!!")

text = args.command if args.file is None else args.file.read_text()

interpreter.interpret(parser.parse(text))

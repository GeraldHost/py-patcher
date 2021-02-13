import sys
import json
import argparse
from opcodes import OPS
from objdump import parse
from patcher import patch 

def setup():
    parser = argparse.ArgumentParser(description='Automatically patch to a sepcified address')
    parser.add_argument('-t', '--target', help='Target address to patch to')
    args = parser.parse_args()

    if not args.target:
        parser.error('The argument --target (-t) is required.')

    return args

if __name__ == "__main__":
    args = setup()

    target_addr = args.target

    binary = parse(sys.stdin)
    patch(binary, target_addr)

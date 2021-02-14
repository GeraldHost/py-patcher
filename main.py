import sys
import json
import argparse
from opcodes import OPS
from objdump import process 
from patcher import patch 

def setup():
    parser = argparse.ArgumentParser(description='Automatically patch to a sepcified address')
    parser.add_argument('-t', '--target', help='Target address to patch to')
    parser.add_argument('-f', '--file', help='Object dump file "objdump -d"')
    args = parser.parse_args()

    if not args.target:
        parser.error('The argument --target (-t) is required.')

    return args

if __name__ == "__main__":
    args = setup()

    target_addr = args.target
    objdump_file = args.file

    with open(objdump_file) as f:
        binary = process(f)
        patch(binary, target_addr)

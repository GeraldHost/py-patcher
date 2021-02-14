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

def print_header():
    print('''
  ___  _ _____ ___ _  _   __  __ ___   _____ _  _ ___  ___  _   _  ___ _  _ 
 | _ \/_\_   _/ __| || | |  \/  | __| |_   _| || | _ \/ _ \| | | |/ __| || |
 |  _/ _ \| || (__| __ | | |\/| | _|    | | | __ |   / (_) | |_| | (_ | __ |
 |_|/_/ \_\_| \___|_||_| |_|  |_|___|   |_| |_||_|_|_\\___/ \___/ \___|_||_|
                                                                            
    ''')
if __name__ == "__main__":
    args = setup()

    target_addr = args.target
    objdump_file = args.file
    
    print_header()

    with open(objdump_file) as f:
        binary = process(f)
        patch(binary, target_addr)

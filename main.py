import sys
import json
import argparse
from opcodes import OPS
from objdump import process 
from patcher import patch 
from whaaaaat import prompt, print_json

header = '''
  ___  _ _____ ___ _  _   __  __ ___   _____ _  _ ___  ___  _   _  ___ _  _ 
 | _ \/_\_   _/ __| || | |  \/  | __| |_   _| || | _ \/ _ \| | | |/ __| || |
 |  _/ _ \| || (__| __ | | |\/| | _|    | | | __ |   / (_) | |_| | (_ | __ |
 |_|/_/ \_\_| \___|_||_| |_|  |_|___|   |_| |_||_|_|_\\___/ \___/ \___|_||_|
                                                                            
'''

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
    
    print(header)

    with open(objdump_file) as f:
        binary = process(f)
        patcher = patch(binary, target_addr)

    confirm_cont = [{
        'type': 'confirm',
        'name': 'continue',
        'message': 'Do you want to apply another patch?'
    }]
    
    while True:
        choices = [{ "name": line.asm, "value": line, "disabled": line.patched } for line in patcher.jumps]

        if len(list(filter(lambda x: not x['disabled'], choices))) <= 0:
            break

        select_jump = [{
            'type': 'list',
            'name': 'patch_jump',
            'message': 'Select jump to patch:',
            'choices': choices
        }]
        answer = prompt(select_jump)
        print(f"Applying patch to: {answer['patch_jump'].asm}")
        answer['patch_jump'].patched = True 

        answer = prompt(confirm_cont)
        if not answer['continue']:
            break

    print("[*] Patching complete")


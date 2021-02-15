import sys
import json
import argparse
import os
from objdump import process
from patcher import patch, write_patch
from whaaaaat import prompt, print_json

header = '''
  ___  _ _____ ___ _  _   __  __ ___   _____ _  _ ___  ___  _   _  ___ _  _ 
 | _ \/_\_   _/ __| || | |  \/  | __| |_   _| || | _ \/ _ \| | | |/ __| || |
 |  _/ _ \| || (__| __ | | |\/| | _|    | | | __ |   / (_) | |_| | (_ | __ |
 |_|/_/ \_\_| \___|_||_| |_|  |_|___|   |_| |_||_|_|_|\___/ \___/ \___|_||_|
                                                                            
'''


def setup():
    parser = argparse.ArgumentParser(
        description='Automatically patch to a sepcified address')
    parser.add_argument('-t', '--target', help='Target address to patch to')
    parser.add_argument('-f', '--file', help='Binary file to patch')
    args = parser.parse_args()

    if not args.target:
        parser.error('The argument --target (-t) is required.')

    if not args.file:
        parser.error('The argument --file (-f) is required.')

    return args


if __name__ == "__main__":
    args = setup()
    target_addr = args.target
    binary_file = args.file

    print(header)

    with os.popen(f"objdump -M intel -d {binary_file}") as f:
        binary = process(f)
        patcher = patch(binary, target_addr)

    confirm_cont = [{
        'type': 'confirm',
        'name': 'continue',
        'message': 'Do you want to apply another patch?'
    }]

    jumps_to_patch = []

    while True:
        choices = [{
            "name": f"{line.offset} :: {line.asm}",
            "value": line,
            "disabled": line.patched
        } for line in patcher.jumps]

        if len(list(filter(lambda x: not x['disabled'], choices))) <= 0:
            break

        select_jump = [{
            'type': 'list',
            'name': 'patch_jump',
            'message': 'Select jump to patch:',
            'choices': choices
        }]

        answer = prompt(select_jump)
        jump_line = answer['patch_jump']
        print(f"[*] Applying patch to: {jump_line.asm}")
        jump_line.patched = True
        jumps_to_patch.append(jump_line)

        answer = prompt(confirm_cont)
        if not answer['continue']:
            break

    write_patch(binary_file, jumps_to_patch)
    print("[*] Patched through :: complete")

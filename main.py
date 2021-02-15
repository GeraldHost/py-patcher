import sys
import json
import argparse
import os
from objdump import process
from patcher import patch, write_patch
from whaaaaat import prompt, print_json
from binary import Binary
from itertools import product 
from utils import str2bool

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
    parser.add_argument('-z', '--fuzz', default=False, type=str2bool, nargs="?", const=True, help='Bool to fuzz for the patch')
    args = parser.parse_args()

    if not args.target:
        parser.error('The argument --target (-t) is required.')

    if not args.file:
        parser.error('The argument --file (-f) is required.')

    return args

def manual_patch(patcher):
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

    return [jumps_to_patch]

def fuzz_patches(patcher):
    print("[*] Attempting to fuzz patch")
    ret = []
    combos = product([1,0], repeat=len(patcher.jumps))
    for combo in combos:
        accum = []
        for i, jump in enumerate(patcher.jumps):
            if combo[i] == 1:
                accum.append(jump)
        ret.append(accum)
    return ret
        

# todo write temp file to test patch
# if patch is successful then write name-patched
# delete temp file
if __name__ == "__main__":
    args = setup()
    target_addr = args.target
    binary_file_path = args.file
    fuzz = args.fuzz

    print(header)

    with os.popen(f"objdump -M intel -d {binary_file_path}") as f:
        binary = process(f)
        patcher = patch(binary, target_addr)
    
    patches = manual_patch(patcher) if not fuzz else fuzz_patches(patcher)
    
    binary = Binary(binary_file_path)
    binary.create_tmp_file()

    worked = binary.try_patches(patches)

    if worked:
        print("[*] Patch succeeded")
    else:
        print("[*] patch failed") 
        binary.cleanup()

    print("[*] Patched through :: complete")

import sys
import re

def hexstr_to_hex(s):
    return hex(int(s, base=16))

def parse_offset(n):
    n = n[:-1] if n[-1] == ":" else n
    return hexstr_to_hex(n)

def parse_instr_bytes(bytes_str):
    return [hexstr_to_hex(n) for n in bytes_str.split()]

def parse_line(line):
    line = line.rstrip('\n').lstrip()
    line = line.replace('\t', '  ')

    items = re.split('\\s{2,}', line)

    offset = parse_offset(items[0])
    instr_bytes = parse_instr_bytes(items[1])

    return offset, instr_bytes

def parse(stdin):
    for line in stdin:
        offset, instr_bytes = parse_line(line)
        print(offset, instr_bytes)

if __name__ == "__main__":
    parse(sys.stdin)

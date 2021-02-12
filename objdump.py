import sys
import re

line_re = re.compile('([0-9a-zA-Z]+:)(\\t*\\s*)(([a-zA-Z0-9]{2}\\s)+)')
section_title_re = re.compile('[0-9A-Za-z]{16}\\s+<(.*[^>])>')

def hexstr_to_hex(s):
    return hex(int(s, base=16))


def parse_offset(n):
    n = n[:-1] if n[-1] == ":" else n
    return hexstr_to_hex(n)


def parse_instr_bytes(bytes_str):
    return [hexstr_to_hex(n) for n in bytes_str.split()]

def parse_asm(asm_str):
    asm = asm_str.split('#')[0].strip()
    print(asm.split(' '))
    return asm

def parse_line(line):
    line = line.rstrip('\n').lstrip()
    line = line.replace('\t', '  ')

    items = re.split('\\s{2,}', line)

    offset = parse_offset(items[0])
    instr_bytes = parse_instr_bytes(items[1])
    asm = parse_asm(' '.join(items[2:]))

    return offset, instr_bytes, asm

def parse_section(line):
    line = line.strip()
    items = line.split(' ')
    
    name_match = re.match('<(.*[^>])>', items[1])
    name = name_match.groups()[0]
    offset = hexstr_to_hex(items[0])
    
    return offset, name

def parse(objdump):
    ret = {}
    curr_name = None
    for line in objdump:
        line = line.strip()
        if section_title_re.match(line):
            offset, name = parse_section(line)
            ret[name] = { "offset": offset, "name": name, "instructions": [] }
            curr_name = name
        elif line_re.match(line):
            print(line)
            offset, instr_bytes, asm = parse_line(line)
            ret[curr_name]['instructions'].append({"offset": offset, "instr_bytes": instr_bytes, "asm": asm })
        else:
            continue
    return ret

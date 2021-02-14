import sys
import re
import json
from utils import hexstr_to_hex

line_re = re.compile('([0-9a-zA-Z]+:)(\\t*\\s*)(([a-zA-Z0-9]{2}\\s)+)')
section_title_re = re.compile('[0-9A-Za-z]{16}\\s+<(.*[^>])>')

# Instruction line
class Line:
    def __init__(self, line_str):
        self.str = line_str
        self.offset = None
        self.bytes = None
        self.asm = None

        self.parse()

    def parse(self):
        line = self.str.rstrip('\n').lstrip()
        line = line.replace('\t', '  ')
        items = re.split('\\s{2,}', line)

        self.offset = self.parse_offset(items[0])
        self.bytes = self.parse_bytes(items[1])
        self.asm = self.parse_asm(' '.join(items[2:]))
    
    @staticmethod
    def parse_offset(n):
        n = n[:-1] if n[-1] == ":" else n
        return hexstr_to_hex(n)
    
    @staticmethod
    def parse_bytes(bytes_str):
        return [hexstr_to_hex(n) for n in bytes_str.split()]
    
    @staticmethod
    def parse_asm(asm_str):
        asm = asm_str.split('#')[0].strip()
        return asm


# Section line
class Section:
    def __init__(self, line_str):
        self.str = line_str
        self.name = None
        self.offset = None
        self.lines = []

        self.parse()

    def parse(self):
        line = self.str.strip()
        items = line.split(' ')
        
        name_match = re.match('<(.*[^>])>', items[1])
        self.name = name_match.groups()[0]
        self.offset = hexstr_to_hex(items[0])

    def addline(self, line):
        self.lines.append(line)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def process(objdump):
    ret = {}
    curr_offset = None
    for ln in objdump:
        ln = ln.strip()
        if section_title_re.match(ln):
            section = Section(ln)
            curr_offset = section.offset
            ret[curr_offset] = section 
        elif line_re.match(ln):
            line = Line(ln)
            ret[curr_offset].addline(line)
        else:
            continue
    return ret

import sys
import re
import json

line_re = re.compile('([0-9a-zA-Z]+:)(\\t*\\s*)(([a-zA-Z0-9]{2}\\s)+)')
section_title_re = re.compile('[0-9A-Za-z]{16}\\s+<(.*[^>])>')

def hexstr_to_hex(s):
    return hex(int(s, base=16))

# Instruction line
class Line:
    def __init__(self, line_str):
        self.str = line_str
        self.offset = None
        self.instr_bytes = None
        self.asm = None

        self.parse()

    def parse(self):
        line = self.str.rstrip('\n').lstrip()
        line = line.replace('\t', '  ')
        items = re.split('\\s{2,}', line)

        self.offset = self.parse_offset(items[0])
        self.instr_bytes = self.parse_instr_bytes(items[1])
        self.asm = self.parse_asm(' '.join(items[2:]))
    
    @staticmethod
    def parse_offset(n):
        n = n[:-1] if n[-1] == ":" else n
        return hexstr_to_hex(n)
    
    @staticmethod
    def parse_instr_bytes(bytes_str):
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
        self.instructions = []

        self.parse()

    def parse(self):
        line = self.str.strip()
        items = line.split(' ')
        
        name_match = re.match('<(.*[^>])>', items[1])
        self.name = name_match.groups()[0]
        self.offset = hexstr_to_hex(items[0])

    def addline(self, line):
        self.instructions.append(line)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def process(objdump):
    ret = {}
    curr_name = None
    for ln in objdump:
        ln = ln.strip()
        if section_title_re.match(ln):
            section = Section(ln)
            curr_name = section.name
            ret[curr_name] = section 
        elif line_re.match(ln):
            line = Line(ln)
            ret[curr_name].addline(line)
        else:
            continue
    return ret

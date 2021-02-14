import re
from utils import hexstr_to_hex, hexstr_to_int
from opcodes import JMP_INSTRUCTIONS
from objdump import Section
from whaaaaat import prompt, print_json

class Patcher:
    def __init__(self, binary, offset):
        self.offset = offset
        self.offset_n = hexstr_to_int(offset)
        self.binary = binary
        self.jumps = []

    @staticmethod
    def section_has_caller(section, offset):
        for line in section.lines:
            call_target = Patcher.get_call_target(line.asm) 
            if not call_target:
                continue
            if hexstr_to_int(call_target) == hexstr_to_int(offset):
                return True
        return False
    
    @staticmethod
    def get_call_target(asm):
        matches = re.match('call\\s([0-9a-zA-Z]{4})\\s', asm)
        if matches:
            return matches.groups()[0]

    # Look for calls of the provided offset the provided offset
    # should be a section offset
    def find_callers(self, offset):
        # check if offset is valid section
        valid = False
        for section_offset in self.binary.keys():
            if section_offset == offset:
                valid = True

        if not valid:
            print(f"[*] Invalid offset: {offset}")
            return
        
        sections_with_callers = []
        for section in self.binary.values():
            if self.section_has_caller(section, offset):
                # if the section has a caller to the target offset
                # then we look for jumps in this section
                sections_with_callers.append(section)
        return sections_with_callers

    def scan_jumps(self, section, offset=None):
        patch_to_offset_n = self.offset_n if offset == None else hexstr_to_int(offset)

        lines_count = len(section.lines)
        for i in range(lines_count, 0, -1):
            line = section.lines[i-1]
            offset_n = hexstr_to_int(line.offset)
            if offset_n < patch_to_offset_n:
                # check if this istruction is a jump instruction
                if line.instruction in JMP_INSTRUCTIONS:
                    self.jumps.append(line)

        sections_with_callers = self.find_callers(section.offset)
        for section in sections_with_callers:
            self.scan_jumps(section, section.lines[-1].offset)

    def findoffset(self):
        section_addrs = self.binary.keys()
        print(f"[*] Finding offset: {self.offset}")
        for i, section_addr in enumerate(section_addrs):
            n = hexstr_to_int(section_addr)
            if n >= self.offset_n:
                print(f"[*] Offset found: {self.offset}")
                key = list(section_addrs)[i-1]
                return self.binary[key]

def patch(binary, offset):
    # find address in the binary to check it exists
    # walk backwards and patch any jumps
    patcher = Patcher(binary, offset)
    section = patcher.findoffset()

    if not isinstance(section, Section):
        print("[*] Offset not found")

    patcher.scan_jumps(section)

    questions = [{
        'type': 'list',
        'name': 'patch_jump',
        'message': 'Select jump to patch',
        'choices': [line.asm for line in patcher.jumps],
    }]

    prompt(questions)

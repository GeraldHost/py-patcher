import re
import binascii
from utils import hexstr_to_hex, hexstr_to_int
from opcodes import JMP_INSTRUCTIONS
from objdump import Section

JE_BYTE = b"74"
JNE_BYTE = b"75"    

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
        patch_to_offset_n = self.offset_n if offset == None else hexstr_to_int(
            offset)

        lines_count = len(section.lines)
        for i in range(lines_count, 0, -1):
            line = section.lines[i - 1]
            offset_n = hexstr_to_int(line.offset)
            # check if this istruction is a jump instruction
            if offset_n < patch_to_offset_n and line.instruction in JMP_INSTRUCTIONS:
                self.jumps.append(line)

        sections_with_callers = self.find_callers(section.offset)
        for section in sections_with_callers:
            self.scan_jumps(section, section.lines[-1].offset)

    def findoffset(self):
        print(f"[*] Finding offset: {self.offset}")

        section_addrs = self.binary.keys()
        for i, section_addr in enumerate(section_addrs):
            if hexstr_to_int(section_addr) >= self.offset_n:
                print(f"[*] Offset found: {self.offset}")
                key = list(section_addrs)[i - 1]
                return self.binary[key]


def patch(binary, offset):
    # find address in the binary to check it exists
    # walk backwards and patch any jumps
    patcher = Patcher(binary, offset)
    section = patcher.findoffset()

    if not isinstance(section, Section):
        print("[*] Offset not found")

    patcher.scan_jumps(section)
    return patcher


# Write the patches to the binary
# @param []Lines array of lines to patch
def write_patch(filepath, patches):
    print(f"[*] Writing {len(patches)} patche(s)")

    with open(filepath, 'r+b') as f:
        for line in patches:
            f.seek(hexstr_to_int(line.offset))
            byte = f.read(1)
            
            hexdata = binascii.hexlify(byte)
            replace_byte = JNE_BYTE if hexdata == JE_BYTE else JE_BYTE
            replace_byte = binascii.unhexlify(replace_byte)
            
            f.seek(hexstr_to_int(line.offset))
            f.write(replace_byte)

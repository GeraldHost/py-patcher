from utils import hexstr_to_hex, hexstr_to_int
from objdump import Section

class Patcher:
    def __init__(self, binary, offset):
        self.offset = offset
        self.binary = binary

    def scanbackwards(self, section):
        # scan backwards until we get to to start of the section
        # if we come across and jumps patch them through
        # once we are at the start of the section scan the entire
        # binary looking for calls to the section
        # repeat
        return 0

    def findoffset(self):
        section_addrs = self.binary.keys()
        print(f"[*] Finding offset: {self.offset}")
        offset_n = hexstr_to_int(self.offset)
        for i, section_addr in enumerate(section_addrs):
            n = hexstr_to_int(section_addr)
            if n >= offset_n:
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

from utils import hexstr_to_hex, hexstr_to_int

class Patcher:
    def __init__(self, binary, offset):
        self.offset = offset
        self.binary = binary

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
        print("[*] Offset not found")

def patch(binary, offset):
    # find address in the binary to check it exists
    # walk backwards and patch any jumps
    patcher = Patcher(binary, offset)
    section = patcher.findoffset()

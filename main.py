import sys
from opcodes import OPS
from objdump import parse

if __name__ == "__main__":
    bn = parse(sys.stdin)
    for line in bn:
        for op in line["instr_bytes"]:
            if op not in OPS.keys():
                continue

            if OPS[op] == "CMP":
                print("[*]: Found CMP")
                print(line)

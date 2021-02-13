import sys
from opcodes import OPS
from objdump import process 

if __name__ == "__main__":
    bn = process(sys.stdin)
    for v in bn.values():
        print(v.toJSON())

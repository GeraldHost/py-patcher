import sys
from opcodes import OPS
from objdump import parse
import json

if __name__ == "__main__":
    bn = parse(sys.stdin)
    print(json.dumps(bn))

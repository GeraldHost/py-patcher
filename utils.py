# take hexstr and convert it to a proper hex and 
# guards against 01 as we want 0x01 
def hexstr_to_hex(s):
    return hex(int(s, base=16))

def hexstr_to_int(s):
    return int(s, base=16)

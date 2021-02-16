# take hexstr and convert it to a proper hex and
# guards against 01 as we want 0x01
def hexstr_to_hex(s):
    return hex(int(s, base=16))


def hexstr_to_int(s):
    return int(s, base=16)

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

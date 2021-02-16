import binascii
import os
from shutil import copy 
from subprocess import Popen, PIPE

from .utils import hexstr_to_int

JE_BYTE = b"74"
JNE_BYTE = b"75"    

class Binary:
    def __init__(self, filepath):
        self.filepath = self.remove_ext(filepath)
        self.tmp_filepath = f"{self.filepath}-patched" 
        self.badboy_outputs = self.get_badboy_outputs()
    
    @staticmethod
    def remove_ext(filepath):
        return filepath.split('.')[0]
    
    def create_tmp_file(self):
        copy(self.filepath, self.tmp_filepath)

    def write_patch(self, filepath, patches):
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

    def try_patches(self, patches):
        for patch in patches:
            self.write_patch(self.tmp_filepath, patch)
            worked = self.test_tmp_file()
            if worked:
                return True
        return False

    def get_badboy_outputs(self):
        ret = []
        for arg in ["password", None]:
            try:
                args = filter(lambda x: x != None, [f"./{self.filepath}", arg])
                res = Popen(args, stdout=PIPE)
            except OSError:
                return None 
            res.wait()
            output = res.stdout.read().strip()
            ret.append(output)
        return ret

    def test_tmp_file(self): 
        try:
            args = [f"./{self.tmp_filepath}", "password"]
            res = Popen(args, stdout=PIPE)
        except OSError:
            return False 
        
        res.wait()
        if res.returncode != 0:
            return False

        output = res.stdout.read().strip()
        return output not in self.badboy_outputs
    
    def cleanup(self):
        os.remove(self.tmp_filepath)


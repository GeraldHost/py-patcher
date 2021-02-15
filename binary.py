import binascii
import os
from shutil import copy 
from subprocess import Popen, PIPE
from utils import hexstr_to_int

JE_BYTE = b"74"
JNE_BYTE = b"75"    

class Binary:
    def __init__(self, filepath):
        self.filepath = self.remove_ext(filepath)
        self.tmp_filepath = f"{self.filepath}-patched" 
        self.badboy_output = self.get_badboy_output()
    
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

    def try_patch(self, patches):
        self.write_patch(self.tmp_filepath, patches)
        worked = self.test_tmp_file()
        return worked

    def get_badboy_output(self):
        try:
            args = [f"./{self.filepath}", "password"]
            res = Popen(args, stdout=PIPE)
        except OSError:
            return None 
        res.wait()
        return res.stdout.read()

    def test_tmp_file(self): 
        try:
            args = [f"./{self.tmp_filepath}", "password"]
            res = Popen(args, stdout=PIPE)
        except OSError:
            return False 
        
        res.wait()
        if res.returncode != 0:
            return False

        output = res.stdout.read()
        return output != self.badboy_output
    
    def cleanup(self):
        os.remove(self.tmp_filepath)


# Py Patcher
### Automating patches to binary files
Attempt to write an semi-automated python patcher. Originally the idea was to automatically figure out what jump
instructions need to be patched in order to get to the goodboy function. However this was a total headache. Instead there are two ways
to patch the binary. 

One finds all the jump instructions, lists them out and allows the user to select which ones to patch

The second uses the `--fuzz` flag to try every combination of "jump if equal" and "jump if not equal" commands until it find the combination that leads to the goodboy function.

# Usage
```
git clone https://github.com/GeraldHost/py-patcher && cd py-patcher
```
```
python -m pypatcher --file=<path_to_binary> --target=<goodboy_offset> --fuzz
```

# Screenshot
Running in normal mode where you have to manually select which jump command to patch

<img src="https://i.imgur.com/2DJEMna.png" alt="py-patcher-screenshot" width="60%"/>

Running with the `--fuzz` options enabled where pypatcher will try and fuzz which jump commands need patching to get to
the good boy function

<img src="https://i.imgur.com/A2DQUX8.png" alt="py-patcher-screenshot-2" width="60%"/>

### Notes
- [http://ref.x86asm.net/coder64.html#x48](http://ref.x86asm.net/coder64.html#x48)

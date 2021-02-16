# Py Patcher
Attempt to write an semi-automated python patcher. Originally the idea was to automatically figure out whay jump
instructions need to be patched in order to get to the goodboy function. However this was a total headache. So far
It works so that it finds all the jump instructions that stand in the way of you and the goodboy function and then
you just tell it which one to patch. However that is super lame so the new idea is to FUZZ all possible combinations
of the jump instructions until you end up at the goodboy function

Update: we can now fuzz the jump instructions with `--fuzz`

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

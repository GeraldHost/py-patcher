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
python main.py --file=<path_to_binary> --target=<goodboy_offset> --fuzz
```

# Screenshot
![py-patcher-screenshot](https://i.imgur.com/4KZiZMz.jpg)

### Notes
- [http://ref.x86asm.net/coder64.html#x48](http://ref.x86asm.net/coder64.html#x48)

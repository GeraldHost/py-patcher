from itertools import product 

arr = [3,3,3]
combos = product([1,0], repeat=len(arr))

for combo in combos:
    tmp = [0 for _ in range(len(arr))]
    for i, a in enumerate(arr):
        tmp[i] = a if combo[i] == 0 else "X"
    print(tmp)

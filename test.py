import numpy as np

import string

tab = np.zeros(26)
word = input("rentrer un mot")
flag = "false"

for x in word:
    print(string.ascii_letters.index('a'))
    print(string.ascii_lowercase.index(x))
    if tab[string.ascii_lowercase.index(x)] >= 1:
        flag = "true"
    else:
        tab[string.ascii_lowercase.index(x)] += 1
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
if word == "Aa":
    print("false")
else:
    print(flag)

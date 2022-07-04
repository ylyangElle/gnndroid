import os
from unittest.mock import patch
path = r"G:\gnn\dataset-f\if_apk_has_google\malware.txt"

f = open(path)
lines = f.readlines()
total = 0
for ele in range(0, len(lines)):
    total = total + int(lines[ele])
print(total)
print(len(lines))
f.close()
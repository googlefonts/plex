import sys
import os
import fractions
from fontTools.ttLib import TTFont

path = sys.argv[-1]
ttFont = TTFont(path)

records = {}

look = [1, 2, 3, 4, 6, 16, 17]

for i in look:

    records[i] = {
        1: ttFont["name"].getName(i, 1, 0, 0),
        3: ttFont["name"].getName(i, 3, 1, 0x409),
    }

for i in sorted(records.keys()):
    print(f'"{i}", "{records[i][1] or ""}", "{records[i][3] or ""}"')
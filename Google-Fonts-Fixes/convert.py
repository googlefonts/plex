import sys
import os
import fractions
from fontTools.ttLib import TTFont

path = sys.argv[-2]
outputfolder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", sys.argv[-1])
)
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
filename = os.path.basename(path)
outputpath = os.path.join(outputfolder, filename)
postScriptName = os.path.splitext(filename)[0]
postScriptFamilyname, postScriptStylename = postScriptName.split("-")


ttFont = TTFont(path)

# Replace ®
ttFont["name"].setName(
    ttFont["name"].getName(7, 1, 0, 0).toUnicode().replace("®", "(r)"), 7, 1, 0, 0
)
ttFont["name"].setName(
    ttFont["name"].getName(7, 3, 1, 0x409).toUnicode().replace("®", "(r)"),
    7,
    3,
    1,
    0x409,
)

# # Copyright Notice
# ttFont["name"].setName(
#     "Copyright 2018 The IBM Plex Project Authors (https://github.com/ibm/plex/)",
#     0,
#     1,
#     0,
#     0,
# )
# ttFont["name"].setName(
#     "Copyright 2018 The IBM Plex Project Authors (https://github.com/ibm/plex/)",
#     0,
#     3,
#     1,
#     0x409,
# )

# Get original postScriptName
originalPostScriptName = ttFont["name"].getName(6, 1, 0, 0).toUnicode()

# Replace shortened postScriptname with full postScriptname
for record in ttFont["name"].names:
    ttFont["name"].setName(
        str(
            ttFont["name"].getName(
                record.nameID, record.platformID, record.platEncID, record.langID
            )
        ).replace(originalPostScriptName, postScriptName),
        record.nameID,
        record.platformID,
        record.platEncID,
        record.langID,
    )


# Rename version from 3.2 to 3.002 in name table
head_version = fractions.Fraction(ttFont["head"].fontRevision)
version_extended = str(float(f"{float(head_version):.5f}"))
version_contracted = ".".join(
    [str(x) for x in [int(x) for x in version_extended.split(".")]]
)
for record in ttFont["name"].names:
    ttFont["name"].setName(
        str(
            ttFont["name"].getName(
                record.nameID, record.platformID, record.platEncID, record.langID
            )
        ).replace(version_contracted, version_extended),
        record.nameID,
        record.platformID,
        record.platEncID,
        record.langID,
    )


# Use Typographic Family Name as Family Name
if ttFont["name"].getName(16, 1, 0, 0):
    familyName = ttFont["name"].getName(16, 1, 0, 0).toUnicode()
    ttFont["name"].setName(familyName, 1, 1, 0, 0)
    ttFont["name"].setName(familyName, 1, 3, 1, 0x409)
    ttFont["name"].removeNames(16, 1, 0, 0)
    ttFont["name"].removeNames(16, 3, 1, 0x409)
if ttFont["name"].getName(17, 1, 0, 0):
    styleName = ttFont["name"].getName(17, 1, 0, 0).toUnicode()
    ttFont["name"].setName(styleName, 2, 1, 0, 0)
    ttFont["name"].setName(styleName, 2, 3, 1, 0x409)
    ttFont["name"].removeNames(17, 1, 0, 0)
    ttFont["name"].removeNames(17, 3, 1, 0x409)

# Set PostScript name
ttFont["name"].setName(postScriptName, 6, 1, 0, 0)
ttFont["name"].setName(postScriptName, 6, 3, 1, 0x409)

# Unused, just for reference
# ttFont["head"].macStyle |= 1 << 1  # Set Italic bit
# ttFont["OS/2"].fsSelection &= ~(1 << 5)  # Clear Bold bit
# ttFont["OS/2"].fsSelection &= ~(1 << 6)  # Clear Regular bit
# ttFont["OS/2"].fsSelection |= 1 << 0  # Set Italic bit

fullName = (
    str(ttFont["name"].getName(1, 1, 0, 0))
    + " "
    + str(ttFont["name"].getName(2, 1, 0, 0))
)
print(fullName)

# Set full name
ttFont["name"].setName(fullName, 4, 1, 0, 0)
ttFont["name"].setName(fullName, 4, 3, 1, 0x409)

# Set fsSelection
if " Italic" in fullName:
    ttFont["OS/2"].fsSelection |= 1 << 0  # Set Italic bit
else:
    ttFont["OS/2"].fsSelection &= ~(1 << 0)  # Clear Italic bit

    if " Bold" in fullName:
        ttFont["OS/2"].fsSelection |= 1 << 5  # Set Bold
        ttFont["OS/2"].fsSelection &= ~(1 << 6)  # Clear Regular bit
    else:
        ttFont["OS/2"].fsSelection |= 1 << 6  # Set Regular
        ttFont["OS/2"].fsSelection &= ~(1 << 5)  # Clear Bold bit

ttFont.save(outputpath)

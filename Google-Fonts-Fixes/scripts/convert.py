import sys
import os
import fractions
from fontTools.ttLib import TTFont

path = sys.argv[-2]
outputfolder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", sys.argv[-1])
)
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
filename = os.path.basename(path)
outputpath = os.path.join(outputfolder, filename)
postScriptName = os.path.splitext(filename)[0]
postScriptFamilyname, postScriptStylename = postScriptName.split("-")


ttFont = TTFont(path)

# Get family name
if ttFont["name"].getName(16, 1, 0, 0):
    familyName = ttFont["name"].getName(16, 1, 0, 0).toUnicode()
else:
    familyName = ttFont["name"].getName(1, 1, 0, 0).toUnicode()

# Get style name
if ttFont["name"].getName(17, 1, 0, 0):
    styleName = ttFont["name"].getName(17, 1, 0, 0).toUnicode()
else:
    styleName = ttFont["name"].getName(2, 1, 0, 0).toUnicode()

print(familyName, styleName)

map = {
    "upright": {
        100: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Thin"},
            2: {(1, 0, 0): "Thin", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Thin",
            "fsSelection": 6,
            "macStyle": None,
        },
        200: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraLight"},
            2: {(1, 0, 0): "ExtraLight", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "ExtraLight",
            "fsSelection": 6,
            "macStyle": None,
        },
        300: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Light"},
            2: {(1, 0, 0): "Light", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Light",
            "fsSelection": 6,
            "macStyle": None,
        },
        400: {
            1: "Family Name",
            2: "Regular",
            16: None,
            17: None,
            "fsSelection": 6,
            "macStyle": None,
        },
        500: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Medium"},
            2: {(1, 0, 0): "Medium", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Medium",
            "fsSelection": 6,
            "macStyle": None,
        },
        600: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name SemiBold"},
            2: {(1, 0, 0): "SemiBold", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "SemiBold",
            "fsSelection": 6,
            "macStyle": None,
        },
        700: {
            1: "Family Name",
            2: "Bold",
            16: None,
            17: None,
            "fsSelection": 5,
            "macStyle": 0,
        },
        800: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraBold"},
            2: {(1, 0, 0): "ExtraBold", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "ExtraBold",
            "fsSelection": 6,
            "macStyle": None,
        },
        900: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Black"},
            2: {(1, 0, 0): "Black", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Black",
            "fsSelection": 6,
            "macStyle": None,
        },
    },
    "italic": {
        100: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Thin"},
            2: {(1, 0, 0): "Thin Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Thin Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        200: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraLight"},
            2: {(1, 0, 0): "ExtraLight Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "ExtraLight Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        300: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Light"},
            2: {(1, 0, 0): "Light Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Light Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        400: {
            1: "Family Name",
            2: "Italic",
            16: None,
            17: None,
            "fsSelection": 0,
            "macStyle": 1,
        },
        500: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Medium"},
            2: {(1, 0, 0): "Medium Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Medium Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        600: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name SemiBold"},
            2: {(1, 0, 0): "SemiBold Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "SemiBold Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        700: {
            1: "Family Name",
            2: "Bold Italic",
            16: None,
            17: None,
            "fsSelection": [5, 0],
            "macStyle": [0, 1],
        },
        800: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraBold"},
            2: {(1, 0, 0): "ExtraBold Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "ExtraBold Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        900: {
            1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Black"},
            2: {(1, 0, 0): "Black Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Black Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
    },
}

# Is it Roman or Italic?
variant = "italic" if "Italic" in styleName else "upright"
weightClass = ttFont["OS/2"].usWeightClass

# Apply style map
if not weightClass in map[variant]:
    raise Exception(f"Weight class {weightClass} is unsupported by this script.")

# Continue
for key in map[variant][weightClass]:
    # Name records
    if type(key) == int:
        # Set name record
        if type(map[variant][weightClass][key]) == str:
            string = map[variant][weightClass][key].replace("Family Name", familyName)
            ttFont["name"].setName(string, key, 1, 0, 0)
            ttFont["name"].setName(string, key, 3, 1, 0x409)
        elif type(map[variant][weightClass][key]) == dict:
            for a, b, c in map[variant][weightClass][key]:
                string = map[variant][weightClass][key][(a, b, c)].replace(
                    "Family Name", familyName
                )
                ttFont["name"].setName(string, key, a, b, c)
        # Delete name record
        elif map[variant][weightClass][key] == None:
            ttFont["name"].removeNames(key, 1, 0, 0)
            ttFont["name"].removeNames(key, 3, 1, 0x409)
    # Other
    elif type(key) == str:

        values = map[variant][weightClass][key]

        # Read
        if key == "fsSelection":

            if type(values) != list:
                values = [values]

            for value in [0, 5, 6]:
                ttFont["OS/2"].fsSelection &= ~(1 << value)

            for value in values:
                if value != None:
                    ttFont["OS/2"].fsSelection |= 1 << value

        elif key == "macStyle":

            if type(values) != list:
                values = [values]

            for value in [0, 1]:
                ttFont["head"].macStyle &= ~(1 << value)

            for value in values:
                if value != None:
                    ttFont["head"].macStyle |= 1 << value


# Get original postScriptName
originalPostScriptName = ttFont["name"].getName(6, 1, 0, 0).toUnicode()

for record in ttFont["name"].names:

    # Replace shortened postScriptname with full postScriptname
    # Replace ® with (r)
    # Replace © with (c)
    ttFont["name"].setName(
        str(
            ttFont["name"].getName(
                record.nameID, record.platformID, record.platEncID, record.langID
            )
        )
        .replace(originalPostScriptName, postScriptName)
        .replace("®", "(r)")
        .replace("©", "(c)"),
        record.nameID,
        record.platformID,
        record.platEncID,
        record.langID,
    )

# Set full name
ttFont["name"].setName(f"{familyName} {styleName}", 4, 1, 0, 0)
ttFont["name"].setName(f"{familyName} {styleName}", 4, 3, 1, 0x409)


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


# # Rename version from 3.2 to 3.002 in name table
# head_version = fractions.Fraction(ttFont["head"].fontRevision)
# version_extended = str(float(f"{float(head_version):.5f}"))
# version_contracted = ".".join(
#     [str(x) for x in [int(x) for x in version_extended.split(".")]]
# )
# for record in ttFont["name"].names:
#     ttFont["name"].setName(
#         str(
#             ttFont["name"].getName(
#                 record.nameID, record.platformID, record.platEncID, record.langID
#             )
#         ).replace(version_contracted, version_extended),
#         record.nameID,
#         record.platformID,
#         record.platEncID,
#         record.langID,
#     )


# # Use Typographic Family Name as Family Name
# if ttFont["name"].getName(16, 1, 0, 0):
#     familyName = ttFont["name"].getName(16, 1, 0, 0).toUnicode()
#     ttFont["name"].setName(familyName, 1, 1, 0, 0)
#     ttFont["name"].setName(familyName, 1, 3, 1, 0x409)
#     ttFont["name"].removeNames(16, 1, 0, 0)
#     ttFont["name"].removeNames(16, 3, 1, 0x409)
# if ttFont["name"].getName(17, 1, 0, 0):
#     styleName = ttFont["name"].getName(17, 1, 0, 0).toUnicode()
#     ttFont["name"].setName(styleName, 2, 1, 0, 0)
#     ttFont["name"].setName(styleName, 2, 3, 1, 0x409)
#     ttFont["name"].removeNames(17, 1, 0, 0)
#     ttFont["name"].removeNames(17, 3, 1, 0x409)

# # Set PostScript name
# ttFont["name"].setName(postScriptName, 6, 1, 0, 0)
# ttFont["name"].setName(postScriptName, 6, 3, 1, 0x409)

# Unused, just for reference
# ttFont["head"].macStyle |= 1 << 1  # Set Italic bit
# ttFont["OS/2"].fsSelection &= ~(1 << 5)  # Clear Bold bit
# ttFont["OS/2"].fsSelection &= ~(1 << 6)  # Clear Regular bit
# ttFont["OS/2"].fsSelection |= 1 << 0  # Set Italic bit

# fullName = (
#     str(ttFont["name"].getName(1, 1, 0, 0))
#     + " "
#     + str(ttFont["name"].getName(2, 1, 0, 0))
# )


ttFont.save(outputpath)
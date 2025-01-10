import sys
import os
from fontTools.ttLib import TTFont
import axisregistry
import json


def get_name(nameID):
    for name in ttFont["name"].names:
        if name.nameID == nameID:
            return name.toUnicode()
    return None


def set_name(nameID, value):
    if value != get_name(nameID):
        print(
            "Replacing",
            nameID,
            get_name(nameID),
            "->",
            value,
        )
    ttFont["name"].setName(value, nameID, 1, 0, 0)
    ttFont["name"].setName(value, nameID, 3, 1, 0x409)


def get_axis(tag):
    for i, axis in enumerate(ttFont["STAT"].table.DesignAxisRecord.Axis):
        if axis.AxisTag == tag:
            return i, axis


def highest_name_ID():
    return max([name.nameID for name in ttFont["name"].names])


def get_version(string):
    return float(string.split(";")[0].split("Version ")[1])


def version_string(version):
    return f"{version:.3f}"


print("===")

# Versions
data = json.load(open("Google-Fonts-Fixes/servers.json", "r"))


path = sys.argv[-2]
ttFont = TTFont(path)

outputfolder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", sys.argv[-1])
)
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)

# Replace names
if "fvar" in ttFont:
    for record in ttFont["name"].names:

        new_name = (
            get_name(record.nameID)
            .replace("IBMPlexSansVar-Roman", "IBMPlexSansVar")
            # .replace("IBMPlexSans-Regular", "IBMPlexSans")
            .replace("IBMPlexSansVar", "IBMPlexSans")
            .replace("IBM Plex Sans Var", "IBM Plex Sans")
        )
        set_name(record.nameID, new_name)

# Get original postScriptName
originalPostScriptName = get_name(6)

if "fvar" in ttFont:
    filename = axisregistry.build_filename(ttFont)
    postScriptNames = get_name(4).split(" ")
    postScriptNames[-1] = "-" + postScriptNames[-1]
    postScriptName = "".join(postScriptNames)
    print(
        "psname:",
        originalPostScriptName,
        "->",
        postScriptName,
        originalPostScriptName == postScriptName,
    )
else:
    filename = os.path.basename(path).replace("-Roman", "-Regular")
    postScriptName = os.path.splitext(filename)[0]

    # Shorten
    postScriptName = postScriptName.replace("Condensed", "Cond").replace("-Roman", "")
    if "-" in postScriptName:
        postScriptName, postScriptStylename = postScriptName.split("-")
    else:
        postScriptStylename = "Regular"

outputpath = os.path.join(outputfolder, filename)


# Get family name
familyName = get_name(16) or get_name(1)

# Get style name
styleName = get_name(17) or get_name(2)

print(familyName, styleName)


# VERSION STRATEGY
if familyName in data["production"]["families"] and get_version(
    data["production"]["families"][familyName]["version"]
):
    production_version = get_version(
        data["production"]["families"][familyName]["version"]
    )
else:
    production_version = 0

assert production_version is not None
incoming_version = get_version(get_name(5))
assert incoming_version

print("VERSION STRATEGY:")
if incoming_version > production_version:
    print(
        f"Incoming version ({incoming_version}) is higher than production version ({production_version}), so use {incoming_version}."
    )
else:
    apply_version = production_version + 0.001
    print(
        f"Incoming version ({incoming_version}) is lower-or-equal than production version ({production_version}), so use prod+.001: {apply_version}"
    )

    # Apply versions
    set_name(
        3,
        get_name(3).replace(
            version_string(incoming_version), version_string(apply_version)
        ),
    )
    set_name(5, f"Version {version_string(apply_version)}")
    ttFont["head"].fontRevision = apply_version


# Complete implementation of https://github.com/googlefonts/gf-docs/tree/main/Spec#supported-styles
map = {
    "upright": {
        100: {
            1: "Family Name Thin",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Thin"},
            # 2: {(1, 0, 0): "Thin", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Thin",
            "fsSelection": 6,
            "macStyle": None,
        },
        200: {
            1: "Family Name ExtraLight",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraLight"},
            # 2: {(1, 0, 0): "ExtraLight", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "ExtraLight",
            "fsSelection": 6,
            "macStyle": None,
        },
        300: {
            1: "Family Name Light",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Light"},
            # 2: {(1, 0, 0): "Light", (3, 1, 0x409): "Regular"},
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
            1: "Family Name Medium",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Medium"},
            # 2: {(1, 0, 0): "Medium", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Medium",
            "fsSelection": 6,
            "macStyle": None,
        },
        600: {
            1: "Family Name SemiBold",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name SemiBold"},
            # 2: {(1, 0, 0): "SemiBold", (3, 1, 0x409): "Regular"},
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
            1: "Family Name ExtraBold",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraBold"},
            # 2: {(1, 0, 0): "ExtraBold", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "ExtraBold",
            "fsSelection": 6,
            "macStyle": None,
        },
        900: {
            1: "Family Name Black",
            2: "Regular",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Black"},
            # 2: {(1, 0, 0): "Black", (3, 1, 0x409): "Regular"},
            16: "Family Name",
            17: "Black",
            "fsSelection": 6,
            "macStyle": None,
        },
    },
    "italic": {
        100: {
            1: "Family Name Thin",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Thin"},
            # 2: {(1, 0, 0): "Thin Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Thin Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        200: {
            1: "Family Name ExtraLight",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraLight"},
            # 2: {(1, 0, 0): "ExtraLight Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "ExtraLight Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        300: {
            1: "Family Name Light",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Light"},
            # 2: {(1, 0, 0): "Light Italic", (3, 1, 0x409): "Italic"},
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
            1: "Family Name Medium",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Medium"},
            # 2: {(1, 0, 0): "Medium Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "Medium Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        600: {
            1: "Family Name SemiBold",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name SemiBold"},
            # 2: {(1, 0, 0): "SemiBold Italic", (3, 1, 0x409): "Italic"},
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
            1: "Family Name ExtraBold",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name ExtraBold"},
            # 2: {(1, 0, 0): "ExtraBold Italic", (3, 1, 0x409): "Italic"},
            16: "Family Name",
            17: "ExtraBold Italic",
            "fsSelection": 0,
            "macStyle": 1,
        },
        900: {
            1: "Family Name Black",
            2: "Italic",
            # 1: {(1, 0, 0): "Family Name", (3, 1, 0x409): "Family Name Black"},
            # 2: {(1, 0, 0): "Black Italic", (3, 1, 0x409): "Italic"},
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

            # Unset bits
            for value in [0, 5, 6]:
                ttFont["OS/2"].fsSelection &= ~(1 << value)

            # Set bits
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

print(
    "psname2",
    originalPostScriptName,
    postScriptName,
    originalPostScriptName == postScriptName,
)

for record in ttFont["name"].names:

    # Replace shortened postScriptname with full postScriptname
    # Replace ® with (r)
    # Replace © with (c)
    new_name = (
        get_name(record.nameID)
        .replace(originalPostScriptName, postScriptName)
        .replace("-Regular-Regular", "-Regular")
        .replace("®", "(r)")
        .replace("©", "(c)")
    )
    set_name(record.nameID, new_name)


if "fvar" in ttFont:
    for record in ttFont["name"].names:

        if record.nameID >= 256:
            new_name = (
                get_name(record.nameID)
                .replace("ExtLt", "ExtraLight")
                .replace("Medm", "Medium")
                .replace("SmBld", "SemiBold")
            )
            if "Cond" in new_name and "Condensed" not in new_name:
                new_name = new_name.replace("Cond", "Condensed")
            if "Ita" in new_name and "Italic" not in new_name:
                new_name = new_name.replace("Ita", "Italic")
            new_name = new_name.replace("RegularItalic", "Italic")
            set_name(record.nameID, new_name)

# Set full name
set_name(4, f"{familyName} {styleName}")

# Set PostScript Name (VF)
if "fvar" in ttFont:
    set_name(6, postScriptName)

# Sad but true, drop all Mac names
for record in ttFont["name"].names:
    if record.platformID == 1:
        ttFont["name"].removeNames(record.nameID, 1, 0, 0)

# General vertical metric adjustments only for non-CJK fonts:
if familyName not in ["IBM Plex Sans KR", "IBM Plex Sans JP"]:
    ttFont["OS/2"].sTypoAscender = ttFont["hhea"].ascent
    ttFont["OS/2"].sTypoDescender = ttFont["hhea"].descent
    ttFont["OS/2"].sTypoLineGap = ttFont["hhea"].lineGap
    ttFont["OS/2"].version = 4  # Enable setting of fsSelection bit 7
    ttFont["OS/2"].fsSelection |= 1 << 7  # Use Typo Metrics

# Custom adjustments for each family according to fontbakery reports
if familyName == "IBM Plex Serif":
    ttFont["OS/2"].usWinAscent = 1150
    ttFont["OS/2"].usWinDescent = 286

if familyName == "IBM Plex Sans Arabic":
    ttFont["OS/2"].usWinAscent = 1128
    ttFont["OS/2"].usWinDescent = 601

if familyName == "IBM Plex Sans Hebrew":
    ttFont["OS/2"].usWinDescent = 365

if familyName == "IBM Plex Sans Devanagari":
    ttFont["OS/2"].usWinAscent = 1099
    ttFont["OS/2"].usWinDescent = 488

if familyName == "IBM Plex Sans KR":
    ttFont["OS/2"].sTypoAscender = 880
    ttFont["OS/2"].sTypoDescender = -120
    ttFont["OS/2"].sTypoLineGap = 0

if familyName == "IBM Plex Sans Thai Looped":
    ttFont["OS/2"].usWinAscent = 1239

if familyName == "IBM Plex Sans JP":
    ttFont["OS/2"].sTypoAscender = 880
    ttFont["OS/2"].sTypoDescender = -120
    ttFont["OS/2"].sTypoLineGap = 0

if familyName == "IBM Plex Sans":  # (Includes VAR)
    ttFont["OS/2"].usWinAscent = 1120

# Delete forbidden fvar instances
if "fvar" in ttFont:
    fvar = ttFont["fvar"]
    for instance in fvar.instances.copy():
        if (
            get_name(instance.subfamilyNameID)
            not in axisregistry.GF_STATIC_STYLES.keys()
        ):
            print(f"Deleting {get_name(instance.subfamilyNameID)} from fvar")
            fvar.instances.remove(instance)
    ttFont["fvar"] = fvar

# STAT
deletes = ["Text"]
if "STAT" in ttFont:
    stat = ttFont["STAT"]
    for value in stat.table.AxisValueArray.AxisValue.copy():
        for delete in deletes:
            if delete in get_name(value.ValueNameID):
                print(f"Deleting {get_name(value.ValueNameID)} from STAT")
                stat.table.AxisValueArray.AxisValue.remove(value)

    for axisValue in stat.table.AxisValueArray.AxisValue:

        # Setting new name IDs below because I found that more than one
        # data point were using the name "Regular" and all pointing
        # # to the same name ID

        # wdth Regular->Normal
        if (
            axisValue.AxisIndex == get_axis("wdth")[0]
            and get_name(axisValue.ValueNameID) == "Regular"
        ):
            newID = highest_name_ID() + 1
            print(newID, "Normal")
            set_name(newID, "Normal")
            axisValue.ValueNameID = newID

        # wdth Condensed 85->75
        # TODO:
        # maybe rewrite this to use axisregistry to assign the correct value by the name
        if axisValue.AxisIndex == get_axis("wdth")[0] and "Condensed" in get_name(
            axisValue.ValueNameID
        ):
            axisValue.Value = 75.0
            ttFont["fvar"].axes[axisValue.AxisIndex].minValue = 75.0

    ttFont["STAT"] = stat

    # Set default instance PS name
    for axisValue in stat.table.AxisValueArray.AxisValue:
        if (
            axisValue.AxisIndex == get_axis("wdth")[0]
            and get_name(axisValue.ValueNameID) == "Regular"
        ):
            newID = highest_name_ID() + 1
            set_name(newID, "Normal")
            axisValue.ValueNameID = newID


ttFont.save(outputpath)

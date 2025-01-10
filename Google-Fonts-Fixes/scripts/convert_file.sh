INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

# rm $OUTPUT
# set -e

echo "Converting $INPUT to $OUTPUT"
python3 Google-Fonts-Fixes/scripts/convert.py "$INPUT" "$OUTPUT"


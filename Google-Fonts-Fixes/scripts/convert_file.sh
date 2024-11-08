INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

# rm $OUTPUT
# set -e

echo "Converting $INPUT to $OUTPUT";
python3 Google-Fonts-Fixes/scripts/convert.py "$INPUT" "$OUTPUT";

gftools fix-nonhinting $OUTPUT/$(basename $INPUT) $OUTPUT/$(basename $INPUT).fix > /dev/null;
mv $OUTPUT/$(basename $INPUT).fix $OUTPUT/$(basename $INPUT);

rm $OUTPUT/*-backup-*

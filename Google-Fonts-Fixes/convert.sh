INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/IBM-Plex-Sans/fonts/complete/ttf"

rm $OUTPUT/*.ttf
set -e

for i in $INPUT/*.ttf; do
    python3 Google-Fonts-Fixes/convert.py $i $OUTPUT;
done

# After burner
for i in $OUTPUT/*.ttf; do
    echo "Fixing hinting of $i"
    gftools fix-nonhinting $i $i.fix > /dev/null;
    mv $i.fix $i;
done

rm $OUTPUT/*-backup-*

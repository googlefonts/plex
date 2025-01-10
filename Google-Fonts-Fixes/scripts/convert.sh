INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

# Download font versions
curl https://raw.githubusercontent.com/googlefonts/gf-dashboard/refs/heads/main/docs/servers.json > Google-Fonts-Fixes/servers.json

rm $OUTPUT/*.ttf
# set -e

for i in $INPUT/*.ttf; do
    echo Input: $i, Output: $OUTPUT;
    sh Google-Fonts-Fixes/scripts/convert_file.sh "$i" "$OUTPUT";
done

for i in $OUTPUT/*.ttf; do
    gftools fix-nonhinting $i $i.fix > /dev/null
    mv $i.fix $i
done

rm $OUTPUT/*-backup-*.ttf

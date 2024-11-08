INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

# Download font versions
curl https://raw.githubusercontent.com/googlefonts/gf-dashboard/refs/heads/main/docs/servers.json > Google-Fonts-Fixes/servers.json

rm $OUTPUT/*.ttf
# set -e

for i in $INPUT/*.ttf; do
    echo $i;
    python3 Google-Fonts-Fixes/scripts/convert.py "$i" "$OUTPUT";
done

for i in $OUTPUT/*.ttf; do
    gftools fix-nonhinting "$i" "$i.fix";
    mv $i.fix $i;
done


# # After burner
# for i in $OUTPUT/*.ttf; do
#     echo "Fixing hinting of $i"
#     gftools fix-nonhinting $i $i.fix > /dev/null;
#     mv $i.fix $i;
# done

rm $OUTPUT/*-backup-*

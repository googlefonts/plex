INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
OUTPUT=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

# Download font versions
curl https://raw.githubusercontent.com/googlefonts/gf-dashboard/refs/heads/main/docs/servers.json > Google-Fonts-Fixes/servers.json

rm $OUTPUT/*.ttf
# set -e

for i in $INPUT/*.ttf; do
    echo $i;
    sh Google-Fonts-Fixes/scripts/convert_file.sh $i $OUTPUT;
done

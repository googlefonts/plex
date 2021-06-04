INPUT=$1 # "IBM-Plex-Sans/fonts/complete/ttf"

for i in $INPUT/*.ttf; do
    python3 list.py $i;
done

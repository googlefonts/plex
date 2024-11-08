UPSTREAM=$1 # "IBM-Plex-Sans/fonts/complete/ttf"
PRODUCTION=$2 # "Google-Fonts-Fixes/fonts/IBM-Plex-Sans/fonts/complete/ttf"

for i in $UPSTREAM/*.ttf; do
    echo "$i";
    ttx -t GPOS -t GDEF -t GSUB -t glyf -t cmap "$i";
done

for i in $PRODUCTION/*.ttf; do
    echo "$i";
    ttx -t GPOS -t GDEF -t GSUB -t glyf -t cmap "$i";
done

for i in $UPSTREAM/*.ttx; do
    if [ -f "${PRODUCTION}/$(basename $i)" ]; then
        diff "$i" "${PRODUCTION}/$(basename $i)" > /dev/null;
        if [ $? -ne 0 ]; then
            echo "#### Update needed for $i";
            sh Google-Fonts-Fixes/scripts/convert_file.sh "${i%.ttx}.ttf" "${PRODUCTION}"
        fi
    fi
    rm $i;
    rm ${PRODUCTION}/$(basename $i);
done

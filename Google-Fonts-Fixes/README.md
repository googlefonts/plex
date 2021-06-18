This folder contains scripts and files that constitute a deviation from the original IBM files for the purpose of pulication of Google Fonts.

The idea is that the original files remain in place, can be updated from the upstream when they change (hoping that the locations remain in place), and Google runs the hotfix scripts over them in order to publish updates.

# Usage

1. Pull latest fonts from upstream: `git merge upstream/main`
2. From the repo’s root folder, run `sh Google-Fonts-Fixes/scripts/convert-sans.sh` (adjust for other families) in the command line.



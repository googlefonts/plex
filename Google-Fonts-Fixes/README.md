This folder contains scripts and files that constitute a deviation from the original IBM files for the purpose of pulication of Google Fonts.

The idea is that the original files remain in place, can be updated from the upstream when they change (hoping that the locations remain in place), and Google runs the hotfix scripts over them in order to publish updates.

# Usage

1. Pull latest fonts from upstream: `git merge upstream/main`
2. From the repo’s root folder, run `sh Google-Fonts-Fixes/scripts/convert-sans.sh` (adjust for other families) in the command line.


# Version Strategy

Ideally, the versions hosted on Google Fonts should be identical with the latest versions published by IBM.

However, at some point something went wrong with the versions on Google Fonts and they are terribly out-of-sync with IBM: higher, but in an inconsistent manner.

Therefore, the conversion script will follow the following strategy:

1. If the latest IBM version is higher than the latest GF production version, use the IBM version.
2. If the latest IBM version is lower or equal than the latest GF production version, increase the GF version by 0.001 increment until eventually the IBM versions will outpace the GF versions and they will be in sync again.

Sorry for the confusion and inconvenience
- Yanone
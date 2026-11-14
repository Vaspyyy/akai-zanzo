#!/usr/bin/env bash
# Download the lettering font (Anime Ace 2.0 BB by Nate Piekos / Blambot) into
# production/fonts/anime-ace-2/. The font is free for independent comics and
# non-profit use but may NOT be redistributed, so it is gitignored: run this
# once per machine.
set -euo pipefail
cd "$(dirname "$0")"
dir=anime-ace-2
if [ -f "$dir/animeace2_reg.ttf" ]; then echo "already there: $dir"; exit 0; fi
tmp="$(mktemp -d)"
curl -sSL -A "Mozilla/5.0" -o "$tmp/aa.zip" "https://dl.dafont.com/dl/?f=anime_ace_bb"
unzip -q -o "$tmp/aa.zip" -d "$tmp/x"
mkdir -p "$dir"
cp "$tmp"/x/animeace2bb_tt/*.ttf "$dir/"
cp "$tmp/x/animeace2bb_tt/font info.txt" "$dir/LICENSE-font-info.txt"
rm -rf "$tmp"
echo "installed $dir: $(ls "$dir" | tr '\n' ' ')"

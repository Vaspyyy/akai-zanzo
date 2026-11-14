#!/usr/bin/env bash
# Build Chapter N into a grayscale PDF and CBZ (right-to-left reading).
# Usage: ./tools-build.sh 001
# Uses only the final pages: page-NN.png or page-NN-MM.png (spreads).
# Skips page-NN.art.png (unlettered art), *.prev.png (backups) and other extras.
set -euo pipefail
ch="${1:-001}"
src="artwork/pages/chapter-$ch"
out="build"
tmp="$(mktemp -d)"
mkdir -p "$out"
i=0
for f in $(ls "$src" | grep -E '^page-[0-9]+(-[0-9]+)?\.png$' | sort | sed "s|^|$src/|"); do
  i=$((i+1))
  magick "$f" -colorspace Gray -quality 92 "$tmp/$(printf '%03d' "$i").jpg"
done
cat > "$tmp/ComicInfo.xml" <<XML
<?xml version="1.0" encoding="utf-8"?>
<ComicInfo><Series>Akai Zanzo</Series><Number>$((10#$ch))</Number><Manga>YesAndRightToLeft</Manga><LanguageISO>en</LanguageISO><BlackAndWhite>Yes</BlackAndWhite></ComicInfo>
XML
rm -f "$out/akai-zanzo-ch$ch.cbz" "$out/akai-zanzo-ch$ch.pdf"
(cd "$tmp" && zip -q -0 "$OLDPWD/$out/akai-zanzo-ch$ch.cbz" ComicInfo.xml *.jpg)
magick "$tmp"/*.jpg "$out/akai-zanzo-ch$ch.pdf"
rm -rf "$tmp"
echo "built $out/akai-zanzo-ch$ch.cbz and .pdf ($i images)"

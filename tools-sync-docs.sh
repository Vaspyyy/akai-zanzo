#!/usr/bin/env bash
# Copy the finished builds into the owner's documents folder, named for reading:
#   ~/Dokumente/Akai Zanzō/{Manga,Light Novel}/...
# Run after any build; tools-build.sh and novel/build-epub.sh call it at the end.
# Override the target with AZ_DOCS_DIR=/some/path.
set -euo pipefail
cd "$(dirname "$0")"
docs="${AZ_DOCS_DIR:-$(xdg-user-dir DOCUMENTS 2>/dev/null || echo "$HOME/Documents")/Akai Zanzō}"
mkdir -p "$docs/Manga/CBZ (comic apps)" "$docs/Light Novel"

# Manga chapters: title from the script's first line, e.g. # Chapter 2: "Thursday"
for pdf in build/akai-zanzo-ch[0-9][0-9][0-9].pdf; do
  [ -e "$pdf" ] || continue
  ch="${pdf#build/akai-zanzo-ch}"; ch="${ch%.pdf}"
  title="$(head -1 "scripts/chapter-$ch.md" 2>/dev/null | sed -E 's/^#[^"]*"([^"]*)".*/\1/; t; s/.*//')"
  name="Ch $(printf '%02d' "$((10#$ch))")${title:+ - $title}"
  find "$docs/Manga" -name "Ch $(printf '%02d' "$((10#$ch))")*" -delete
  cp "$pdf" "$docs/Manga/$name.pdf"
  [ -e "${pdf%.pdf}.cbz" ] && cp "${pdf%.pdf}.cbz" "$docs/Manga/CBZ (comic apps)/$name.cbz"
done

# Light novel volumes.
for f in build/akai-zanzo-novel-v[0-9][0-9].{pdf,epub}; do
  [ -e "$f" ] || continue
  v="${f#build/akai-zanzo-novel-v}"; ext="${v##*.}"; v="${v%.*}"
  cp "$f" "$docs/Light Novel/Vol $v.$ext"
done

cat > "$docs/Read me first.txt" <<'TXT'
AKAI ZANZŌ (Red Afterimage)

Reading order:
  1. Manga, chapters 1-3 (folder "Manga").
  2. Light novel, volume 1 (folder "Light Novel"). It picks up right after manga chapter 3.
Later manga chapters will adapt the light novel.

PDF works everywhere. EPUB is for ebook apps, CBZ for comic apps (right-to-left).
These files are copies: they are refreshed automatically after every build.
TXT

echo "synced to: $docs"

#!/usr/bin/env bash
# Build the light novel EPUB for one volume.
#
#   novel/build-epub.sh [VOLUME]      (default: 1)
#
# Joins novel/volume-NN/chapter-NN.md in order (plan files are skipped),
# converts them to one HTML book (Python "markdown" module, or Calibre's own
# markdown input if that module is missing), and runs Calibre's ebook-convert.
# Output: build/akai-zanzo-novel-vNN.epub (build/ is gitignored).
# Afterwards it checks the book: ebook-meta, then a round trip to plain text
# that must contain no em dashes and no leftover markdown symbols.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
vol="${1:-1}"
nn="$(printf '%02d' "$((10#$vol))")"
src="$here/volume-$nn"
out="$root/build"
work="$out/novel-v$nn"
epub="$out/akai-zanzo-novel-v$nn.epub"

case "$((10#$vol))" in
  1) vtitle="Good Eyes" ;;
  2) vtitle="Three Months" ;;
  3) vtitle="Eighteen" ;;
  4) vtitle="Odds" ;;
  5) vtitle="Gallery" ;;
  6) vtitle="Three Years" ;;
  7) vtitle="Afterimage" ;;
  *) vtitle="" ;;
esac
title="Akai Zanzō, Volume $((10#$vol))${vtitle:+: $vtitle}"

command -v ebook-convert >/dev/null || { echo "ebook-convert (Calibre) not found" >&2; exit 1; }
shopt -s nullglob
chapters=("$src"/chapter-[0-9][0-9].md)
shopt -u nullglob
[ ${#chapters[@]} -gt 0 ] || { echo "no chapters in $src" >&2; exit 1; }

rm -rf "$work"
mkdir -p "$work"
# illustrations referenced as images/chNN-1.png sit next to the joined book
[ -d "$src/images" ] && cp -r "$src/images" "$work/images"

css='body { font-family: Georgia, "Times New Roman", serif; line-height: 1.5; margin: 0 4%; }
h1 { font-weight: normal; font-size: 1.6em; text-align: center; margin: 3em 0 2em; page-break-before: always; }
p { margin: 0; text-indent: 1.3em; text-align: left; }
h1 + p, p.scene + p, hr + p { text-indent: 0; }
p.scene { text-align: center; text-indent: 0; margin: 1.2em 0; }
hr { width: 20%; margin: 1.2em auto; border: 0; border-top: 1px solid #888; }
em { font-style: italic; }'
printf '%s\n' "$css" > "$work/book.css"

if python3 -c 'import markdown' 2>/dev/null; then
  python3 - "$work/book.html" "$title" "${chapters[@]}" <<'PY'
import html, re, sys
import markdown

out, title, files = sys.argv[1], sys.argv[2], sys.argv[3:]
md = markdown.Markdown(
    extensions=["smarty"],
    # curly quotes and apostrophes only: never turn "--" into dashes, keep "..."
    extension_configs={"smarty": {"smart_dashes": False, "smart_ellipses": False,
                                  "smart_angled_quotes": False, "smart_quotes": True}},
)
parts = []
for f in files:
    text = open(f, encoding="utf-8").read()
    body = md.reset().convert(text)
    # smarty reads a quote before "..." as closing; an opening quote follows a tag or a space
    body = re.sub(r'(^|[\s>(])&rdquo;', r'\1&ldquo;', body, flags=re.M)
    # "* * *" scene breaks: a centred row of dots
    body = re.sub(r"<hr\s*/?>", '<p class="scene">•  •  •</p>', body)
    parts.append(f'<div class="chapter">\n{body}\n</div>')
css = open(out.rsplit("/", 1)[0] + "/book.css", encoding="utf-8").read()
doc = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title>
<style>
{css}
</style></head>
<body>
{chr(10).join(parts)}
</body></html>
"""
open(out, "w", encoding="utf-8").write(doc)
PY
  input="$work/book.html"
  extra=()
else
  echo "python markdown module missing: using Calibre's markdown input" >&2
  for f in "${chapters[@]}"; do cat "$f"; printf '\n\n'; done > "$work/book.md"
  input="$work/book.md"
  extra=(--formatting-type markdown --paragraph-type off --extra-css "$work/book.css")
fi

cover_src="$root/artwork/pages/chapter-001/page-01.png"
cover=()
if [ -f "$cover_src" ]; then
  if command -v magick >/dev/null; then
    magick "$cover_src" -quality 88 "$work/cover.jpg" && cover=(--cover "$work/cover.jpg")
  else
    cover=(--cover "$cover_src")
  fi
fi

ebook-convert "$input" "$epub" \
  "${extra[@]}" "${cover[@]}" \
  --title "$title" --authors "Akai Zanzō" --language en \
  --series "Akai Zanzō" --series-index "$((10#$vol))" \
  --chapter "//h:h1" --chapter-mark pagebreak --page-breaks-before "//h:h1" \
  --level1-toc "//h:h1" --toc-title "Contents" --epub-inline-toc \
  --preserve-cover-aspect-ratio >"$work/convert.log" 2>&1 \
  || { tail -20 "$work/convert.log" >&2; exit 1; }

# Check the result.
ebook-meta "$epub"
ebook-convert "$epub" "$work/roundtrip.txt" >"$work/roundtrip.log" 2>&1
bad=0
if grep -nP '\x{2014}' "$work/roundtrip.txt"; then echo "FAIL: em dash in book" >&2; bad=1; fi
if grep -nE -- '--|^#|\*|^>|`|\]\(|(^|[^a-z])_[A-Za-z]' "$work/roundtrip.txt"; then echo "FAIL: markdown symbols in book" >&2; bad=1; fi
words=$(wc -w < "$work/roundtrip.txt")
echo "chapters: ${#chapters[@]}  words (round trip): $words  size: $(du -h "$epub" | cut -f1)"
echo "built: $epub"

# Phone-sized PDF too: the T3 Code file viewer can't open EPUBs, but shows PDFs.
pdf="${epub%.epub}.pdf"
QT_QPA_PLATFORM=offscreen ebook-convert "$epub" "$pdf" \
  --custom-size 105x180 --unit millimeter --pdf-default-font-size 14 \
  --pdf-page-margin-left 22 --pdf-page-margin-right 22 \
  --pdf-page-margin-top 28 --pdf-page-margin-bottom 28 \
  --pdf-page-numbers >"$work/pdf.log" 2>&1 \
  || { tail -20 "$work/pdf.log" >&2; exit 1; }
echo "built: $pdf"
exit $bad

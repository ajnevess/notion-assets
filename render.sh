#!/bin/zsh
# Renderiza html/*.html -> png/*.png com Chrome headless nas medidas do Notion.
setopt nullglob
cd "$(dirname "$0")"
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p png
for f in html/icon-*.html; do
  "$C" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
       --window-size=280,280 --screenshot="png/$(basename "${f%.html}").png" "file://$PWD/$f" >/dev/null 2>&1
done
for f in html/cover-*.html; do
  "$C" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
       --window-size=1500,600 --screenshot="png/$(basename "${f%.html}").png" "file://$PWD/$f" >/dev/null 2>&1
done
echo "icons $(ls png/icon-*.png | wc -l | tr -d ' ') covers $(ls png/cover-*.png | wc -l | tr -d ' ')"

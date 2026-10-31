#!/usr/bin/env bash
# Keep what the pages load small (the budget is 500 KB per page without video):
#   public/assets/img/<name>.gif       -> <name>.webp: one still from the middle, at most 640 px wide
#   public/assets/video/src/<slot>.*   -> public/assets/video/<slot>.mp4: H.264, at most 720 p,
#                                         faststart (src/ is git-ignored: raw footage stays local)
#   public/assets/video/<slot>.mp4     -> <slot>-poster.jpg, if no poster exists yet
#
#   scripts/optimize_media.sh                 # every GIF and video
#   scripts/optimize_media.sh path/to/x.gif   # just these GIFs
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || { echo "optimize_media: ffmpeg is not installed" >&2; exit 1; }
shopt -s nullglob

size() { printf '%9d B  %s\n' "$(stat -c %s "$1")" "$1"; }

still() {
  local gif=$1 out=${1%.gif}.webp dur
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$gif" || true)
  [[ "$dur" =~ ^[0-9.]+$ ]] || dur=0
  ffmpeg -v error -y -ss "$(awk -v d="$dur" 'BEGIN { printf "%.2f", d / 2 }')" -i "$gif" \
    -frames:v 1 -vf "scale='min(640,iw)':-2:flags=lanczos" -c:v libwebp -quality 80 "$out"
  size "$out"
}

if [ $# -gt 0 ]; then
  for gif in "$@"; do still "$gif"; done
  exit 0
fi

for gif in public/assets/img/*.gif; do still "$gif"; done

for src in public/assets/video/src/*; do
  out=public/assets/video/$(basename "${src%.*}").mp4
  ffmpeg -v error -y -i "$src" -vf "scale=-2:'min(720,ih)'" -c:v libx264 -crf 28 -preset slow \
    -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$out"
  size "$out"
done

for mp4 in public/assets/video/*.mp4; do
  poster=${mp4%.mp4}-poster.jpg
  if [ ! -e "$poster" ]; then
    ffmpeg -v error -y -ss 1 -i "$mp4" -frames:v 1 -vf "scale=-2:'min(720,ih)'" -q:v 4 "$poster"
    size "$poster"
  fi
done

#!/usr/bin/env bash
# Keep what the pages load small (the budget is 500 KB per page without video):
#   public/assets/img/<name>.gif       -> <name>.webp: one still from the middle, at most 640 px wide
#   --video SRC (the full-length Bot & Brew video, kept in public/assets/video/src/, which is
#   git-ignored) -> public/assets/video/bot-and-brew-60s.mp4: the whole cycle at 2x speed, no
#   cutting, 720 p, no audio, H.264, faststart, CRF raised from 24 until the file is <= 8 MB;
#   bot-and-brew-60s-poster.jpg: the frame about 5 s in, <= 150 KB; bot-and-brew-60s.en.vtt:
#   one caption cue spanning the whole clip
#
#   scripts/optimize_media.sh                 # every GIF
#   scripts/optimize_media.sh path/to/x.gif   # just these GIFs
#   scripts/optimize_media.sh --video public/assets/video/src/<full-length>.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || { echo "optimize_media: ffmpeg is not installed" >&2; exit 1; }
shopt -s nullglob

size() { printf '%9d B  %s\n' "$(stat -c %s "$1")" "$1"; }

VIDEO=public/assets/video/bot-and-brew-60s
VIDEO_MAX=8000000   # bytes
POSTER_MAX=150000   # bytes
CAPTION="One autonomous latte cycle, no human intervention — edited from several angles, shown at 2× speed; filmed January 2026."

video() {
  local src=$1 crf=24 q=2 dur
  while :; do
    ffmpeg -v error -y -i "$src" -filter:v "setpts=0.5*PTS,scale=-2:720" -an -c:v libx264 -preset slow \
      -crf "$crf" -movflags +faststart "$VIDEO.mp4"
    echo "crf $crf: $(stat -c %s "$VIDEO.mp4") B"
    [ "$(stat -c %s "$VIDEO.mp4")" -le $VIDEO_MAX ] && break
    crf=$((crf + 1))
  done
  while :; do
    ffmpeg -v error -y -ss 5 -i "$VIDEO.mp4" -frames:v 1 -q:v "$q" "$VIDEO-poster.jpg"
    [ "$(stat -c %s "$VIDEO-poster.jpg")" -le $POSTER_MAX ] && break
    q=$((q + 1))
  done
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO.mp4")
  printf 'WEBVTT\n\n00:00:00.000 --> %s\n%s\n' \
    "$(awk -v d="$dur" 'BEGIN { m = int(d / 60); printf "00:%02d:%06.3f", m, d - 60 * m }')" "$CAPTION" > "$VIDEO.en.vtt"
  size "$VIDEO.mp4"; size "$VIDEO-poster.jpg"; size "$VIDEO.en.vtt"
  echo "crf $crf, poster -q:v $q, duration $dur s"
}

if [ "${1:-}" = --video ]; then
  [ -f "${2:-}" ] || { echo "optimize_media: --video needs the source file" >&2; exit 1; }
  video "$2"
  exit 0
fi

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

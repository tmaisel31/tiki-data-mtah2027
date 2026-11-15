#!/usr/bin/env bash
# Rebuild Tiki Data's submission file ("Tiki Data.csv", possession v3.1) from the organisers' data bundle, and check
# that it is byte for byte the team's file.
#
#     bash reproduce.sh [DATA_DIR] [OUT_DIR]
#
# DATA_DIR  the folder that holds tactical/ (default: $MTAH_DATA_DIR)
# OUT_DIR   where the files are written (default: ~/tiki_data_output); it must be outside this repository
#
# It runs setup/possession_v3_1_standalone.py (which checks Python, the pinned packages and every embedded source and
# model by SHA-256, writes possession_v3_1.csv and validates it), saves the kit's screen to OUT_DIR/kit_screen.txt,
# and compares the kit's FINGERPRINT line (the first 16 hex characters of the file's SHA-256) with
# setup/POSSESSION_V3_1_FINGERPRINT.txt, exactly as step 6 of setup/RUN_THIS_FIRST_v3_1.txt. Only on a match does it
# copy the file to OUT_DIR/"Tiki Data.csv". The last line is
#     V3.1 REBUILD: MATCH (80f4da2a7d76d506)
# or a MISMATCH / STOPPED line (exit 1).
set -u -o pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
DATA="${1:-${MTAH_DATA_DIR:-}}"
OUT="${2:-$HOME/tiki_data_output}"
KIT="$REPO/setup/possession_v3_1_standalone.py"
REFFILE="$REPO/setup/POSSESSION_V3_1_FINGERPRINT.txt"

stop() { echo "V3.1 REBUILD: STOPPED ($1)"; exit 1; }

[ -n "$DATA" ] || stop "no data folder: pass it as the first argument or set MTAH_DATA_DIR"
[ -d "$DATA/tactical" ] || stop "the data folder has no tactical/ folder: pass the folder that holds tactical/"
[ -f "$KIT" ] || stop "setup/possession_v3_1_standalone.py is missing"
[ -f "$REFFILE" ] || stop "setup/POSSESSION_V3_1_FINGERPRINT.txt is missing"
command -v python > /dev/null 2>&1 || stop "python is not on the PATH: activate the environment first"
MADE=0
if [ ! -d "$OUT" ]; then
    mkdir -p "$OUT" || stop "cannot make the output folder"
    MADE=1
fi
OUTR="$(cd "$OUT" && pwd -P)" || stop "cannot open the output folder"
case "$OUTR/" in
    "$REPO/"*)
        [ "$MADE" = 1 ] && rmdir "$OUT" 2> /dev/null
        stop "the output folder is inside this repository: choose a folder outside it" ;;
esac
OUT="$OUTR"

python "$KIT" --data "$DATA" --out "$OUT" | tee "$OUT/kit_screen.txt"
[ "${PIPESTATUS[0]}" -eq 0 ] || stop "the kit refused or failed: read its screen above"

REF=$(sed -n 's/^POSSESSION V3\.1 KIT FINGERPRINT: \([0-9a-f]\{16\}\).*/\1/p' "$REFFILE")
GOT=$(sed -n 's/^POSSESSION V3\.1 KIT FINGERPRINT: \([0-9a-f]\{16\}\)$/\1/p' "$OUT/kit_screen.txt")
if [ -z "$REF" ] || [ "$GOT" != "$REF" ]; then
    echo "V3.1 REBUILD: MISMATCH (yours: ${GOT:-none}, team's: ${REF:-none}); do not use or upload the file"
    exit 1
fi

if command -v shasum > /dev/null 2>&1; then
    SHA=$(shasum -a 256 "$OUT/possession_v3_1.csv" | cut -c1-16)
else
    SHA=$(sha256sum "$OUT/possession_v3_1.csv" | cut -c1-16)
fi
[ "$SHA" = "$REF" ] || stop "the file's SHA-256 does not start with the fingerprint"
cp "$OUT/possession_v3_1.csv" "$OUT/Tiki Data.csv" || stop "cannot write Tiki Data.csv"
cmp -s "$OUT/possession_v3_1.csv" "$OUT/Tiki Data.csv" || stop "the copy differs"
echo "Wrote $OUT/Tiki Data.csv"
echo "V3.1 REBUILD: MATCH ($GOT)"

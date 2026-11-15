#!/usr/bin/env python3
"""CHECK BEFORE PUSH: refuse to publish this repository if it holds anything it must not.

    python3 -I tools/check_before_push.py [REPO_FOLDER]

REPO_FOLDER defaults to the folder above tools/. Two sets of files are checked:
  * every file in the working folder (everything except .git/, ignored files included: a data file lying in the
    folder is already one mistake away from a commit), and
  * every file in the git history (every blob reachable from any branch or tag), because a file that was committed
    and then deleted is still pushed.

It FAILS on:
  M  a match or data file: by name (data folders, the competition's file names, tables such as CSV / TSV / parquet,
     any XML, any TXT except the listed documentation files) or by content (a frame,label table, tracking-style
     frame lines, EPTS / SportsCode-style XML), whatever the file is called;
  V  a video or audio file (by extension or by its first bytes);
  B  a file whose NAME holds the match code BAR-ATH (mentions inside documentation and code are references, allowed);
  R  any real-match aggregate variable (the team's private environment-variable prefix, with any name);
  K  any key or token (private-key blocks; GitHub, AWS, Slack, Google, Hugging Face, OpenAI and Anthropic key shapes;
     a password / secret / token / api_key assigned a literal value);
  P  a home-folder path (/Users/<name>/ or /home/<name>/), which would publish a person's account name;
  S  any file over 50 MB (50,000,000 bytes).

It prints only rule letters, paths and counts, never the text that matched. Last line:
    CHECK BEFORE PUSH: PASS (...)      exit 0
    CHECK BEFORE PUSH: FAIL (...)      exit 1
Standard library only.
"""

import os
import re
import subprocess
import sys

MAX_BYTES = 50_000_000

# documentation / kit TXT files that may be committed (everything else named *.txt is treated as possible match data)
ALLOWED_TXT = {
    "setup/RUN_THIS_FIRST_v3_1.txt",
    "setup/POSSESSION_V3_1_FINGERPRINT.txt",
    "setup/README_POSSESSION_V3_1_LEAD.txt",
    "setup/README_PUBLIC_DATA.txt",
    "setup/requirements_pinned.txt",
}

DATA_DIRS = {"data", "tactical", "private", "bench", "claude_reports", "cache", "public_data", "idsse_dataset",
             "skillcorner"}
DATA_EXT = {".csv", ".tsv", ".parquet", ".feather", ".h5", ".hdf5", ".npy", ".npz", ".pkl", ".pickle", ".xml",
            ".xlsx", ".xls", ".sqlite", ".db", ".part", ".zip", ".tar", ".gz", ".tgz", ".7z", ".bz2", ".xz"}
MEDIA_EXT = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm", ".mpg", ".mpeg", ".mts", ".m2ts", ".wmv", ".flv",
             ".wav", ".mp3", ".aac", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".aiff", ".aif",
             ".png", ".jpg", ".jpeg", ".heic", ".gif", ".bmp", ".tif", ".tiff"}
MATCH_NAME = re.compile(r"bar[-_ ]?ath|tactical_atd|smart[_ -]?tagging|homography", re.I)
BAR_ATH = re.compile(r"bar-ath", re.I)

# content signatures of match data (counted per file; a code or documentation mention is far below these counts)
SUBMISSION_ROW = re.compile(rb"^[0-9]+\s*,\s*[HADXhadx]\s*\r?$", re.M)                     # frame,label rows
TRACKING_ROW = re.compile(rb"^[0-9]+:[-0-9.,NnAa]+(;[-0-9.,NnAa]+){5,}", re.M)               # frame:x,y,s;...
EPTS_TAG = re.compile(rb"<(PlayerChannel|DataSpecification|TrackingDataFormat|FrameRate)\b")
INSTANCE_TAG = re.compile(rb"<instance>")
MEDIA_MAGIC = (b"ftyp", b"RIFF", b"ID3", b"OggS", b"fLaC", b"\x1aE\xdf\xa3")

# the team's private real-aggregate prefix, built so that this file does not contain it
REAL_PREFIX = re.compile(("MTAH" + "_" + "REAL" + "_").encode() + rb"[A-Za-z0-9_]*")

_B = rb"(?<![A-Za-z0-9+/_-])"     # not inside a longer base64 / token run
_E = rb"(?![A-Za-z0-9_-])"
KEY_PATTERNS = [
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(_B + rb"gh[pousr]_[A-Za-z0-9]{36,}" + _E),
    re.compile(_B + rb"github_pat_[A-Za-z0-9_]{40,}" + _E),
    re.compile(_B + rb"(AKIA|ASIA)[0-9A-Z]{16}" + _E),
    re.compile(_B + rb"xox[abposr]-[A-Za-z0-9-]{10,}" + _E),
    re.compile(_B + rb"AIza[0-9A-Za-z_-]{35}" + _E),
    re.compile(_B + rb"hf_[A-Za-z0-9]{30,}" + _E),
    re.compile(_B + rb"sk-ant-[A-Za-z0-9_-]{20,}" + _E),
    re.compile(_B + rb"sk-(proj-)?[A-Za-z0-9]{32,}" + _E),
    re.compile(rb"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|private[_-]?key)"
               rb"\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
    re.compile(rb"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{20,}"),
]
HOME_PATH = re.compile(rb"(?<![A-Za-z0-9_.~-])/(Users|home)/(?!(name|user|username|you|me|runner|<)\b)[A-Za-z0-9._-]+/")


def name_rules(rel, size):
    """Rule letters that a file's path and size alone break."""
    out = set()
    parts = rel.split("/")
    low = rel.lower()
    base = parts[-1]
    ext = os.path.splitext(base)[1].lower()
    if any(p.lower() in DATA_DIRS for p in parts[:-1]):
        out.add("M")
    if ext in DATA_EXT or MATCH_NAME.search(base):
        out.add("M")
    if ext == ".txt" and rel not in ALLOWED_TXT:
        out.add("M")
    if ext in MEDIA_EXT:
        out.add("V")
    if BAR_ATH.search(base):
        out.add("B")
    if size > MAX_BYTES:
        out.add("S")
    if base in (".env",) or low.endswith(".env") or base in ("id_rsa", "id_ed25519", "credentials.json"):
        out.add("K")
    return out


def content_rules(rel, data, self_rel):
    """Rule letters that a file's bytes break (counts only; nothing is printed here)."""
    out = set()
    if data[:12].find(b"ftyp") >= 0 or data.startswith(MEDIA_MAGIC):
        out.add("V")
    if len(SUBMISSION_ROW.findall(data)) >= 1000:
        out.add("M")
    if len(TRACKING_ROW.findall(data)) >= 100:
        out.add("M")
    if len(EPTS_TAG.findall(data)) >= 3 or len(INSTANCE_TAG.findall(data)) >= 20:
        out.add("M")
    if REAL_PREFIX.search(data):
        out.add("R")
    if rel != self_rel and any(p.search(data) for p in KEY_PATTERNS):
        out.add("K")
    if HOME_PATH.search(data):
        out.add("P")
    return out


def working_files(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not (d == root and x == ".git"))
        for f in sorted(files):
            p = os.path.join(d, f)
            if os.path.islink(p):
                yield os.path.relpath(p, root).replace(os.sep, "/"), None
                continue
            yield os.path.relpath(p, root).replace(os.sep, "/"), p


def history_blobs(root):
    """(path, blob sha) for every blob reachable from any ref; [] if the folder is not a git repository."""
    r = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    r = subprocess.run(["git", "-C", root, "rev-list", "--objects", "--all"], capture_output=True, text=True)
    objs = [ln.split(" ", 1) for ln in r.stdout.splitlines() if " " in ln]
    if not objs:
        return []
    r = subprocess.run(["git", "-C", root, "cat-file", "--batch-check=%(objectname) %(objecttype)"],
                       input="\n".join(o[0] for o in objs) + "\n", capture_output=True, text=True)
    kinds = dict(ln.split(" ", 1) for ln in r.stdout.splitlines() if " " in ln)
    return [(path, sha) for sha, path in objs if kinds.get(sha) == "blob"]


def blob_bytes(root, sha):
    return subprocess.run(["git", "-C", root, "cat-file", "blob", sha], capture_output=True).stdout


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(here)
    self_rel = "tools/check_before_push.py"
    fails = {}
    n_work = 0
    for rel, path in working_files(root):
        n_work += 1
        if path is None:
            fails.setdefault(rel, set()).add("M")            # a symbolic link may point at data: refuse it
            continue
        size = os.path.getsize(path)
        rules = name_rules(rel, size)
        with open(path, "rb") as fh:
            rules |= content_rules(rel, fh.read(), self_rel)
        if rules:
            fails.setdefault(rel, set()).update(rules)
    blobs = history_blobs(root)
    n_hist = 0
    if blobs:
        seen = set()
        for rel, sha in blobs:
            if (rel, sha) in seen:
                continue
            seen.add((rel, sha))
            n_hist += 1
            data = blob_bytes(root, sha)
            rules = name_rules(rel, len(data)) | content_rules(rel, data, self_rel)
            if rules:
                fails.setdefault("history:" + rel, set()).update(rules)
    for rel in sorted(fails):
        print("CHECK FAIL [%s] %s" % ("".join(sorted(fails[rel])), rel))
    what = "%d working files, %d committed files%s" % (n_work, n_hist, "" if blobs is not None else ", not a git repository")
    if fails:
        print("  rules: M match/data file, V video/audio/picture, B BAR-ATH file name, R real-match aggregate variable,")
        print("         K key or token, P home-folder path, S over 50 MB")
        print("CHECK BEFORE PUSH: FAIL (%d of them break a rule; %s)" % (len(fails), what))
        return 1
    print("CHECK BEFORE PUSH: PASS (%s)" % what)
    return 0


if __name__ == "__main__":
    sys.exit(main())

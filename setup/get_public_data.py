#!/usr/bin/env python3
"""PUBLIC DATA KIT: our public training data on your own machine, downloaded from the official sources and checked
byte for byte. GENERATED from fetch_public_data.py's own download code and a manifest of our local copies; do not edit
by hand.

    python get_public_data.py --out "/path/to/folder"

It fetches exactly the files our harness and studies read: the 7 public DFL matches (match information, events and
positions, from figshare, the files floodlight's IDSSEDataset loads) into FOLDER/idsse_dataset/, and the 3 SkillCorner
open-data matches (tracking with possession) into FOLDER/skillcorner/. Files that already exist and match are skipped;
the rest are downloaded (to a .part file, renamed only when its size and SHA-256 match) and every file is checked.
Screen: one line per dataset, "PUBLIC DATA <name>: files a of b match", then "PUBLIC DATA READY: yes" or
"PUBLIC DATA READY: no (...)" naming what failed. A network error stops the run with one line. Standard library only.
Read README_PUBLIC_DATA.txt.
"""

import hashlib
import http.client
import os
import sys
import urllib.error
import urllib.request

P = "PUBLIC DATA"
USAGE = P + ": usage: python get_public_data.py --out FOLDER"

# ================================================================ the manifest (generated from our local copies)
DATASETS = [
    ('DFL', [
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000001_DFL-MAT-J03WMX.xml', 11930, 'a884728647a564cf8b20e5223a1d04a5da6f6725e1e506c8651505327c197ba9',
         'https://ndownloader.figshare.com/files/51643475'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000001_DFL-MAT-J03WN1.xml', 11722, '5490286436c86e6f80a538d2b1b379d0efd016e0defcaf594bc59d9ef5079f4c',
         'https://ndownloader.figshare.com/files/51643472'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000002_DFL-MAT-J03WOH.xml', 11745, 'f23b3ee13b988b1ff9a0bce438c416dac47e71355bbc7ee1dab21aaf3e33c18c',
         'https://ndownloader.figshare.com/files/51643478'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000002_DFL-MAT-J03WOY.xml', 11952, '4c497fac683eee8292901c18ca02c0be1d9609d0b9d4bd8aa092c61f9e0b19e9',
         'https://ndownloader.figshare.com/files/51643481'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000002_DFL-MAT-J03WPY.xml', 11922, '566dd5e4c86e124ab90fcdba51100881f0436e22afa71832945a451a2d95a420',
         'https://ndownloader.figshare.com/files/51643487'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000002_DFL-MAT-J03WQQ.xml', 11932, 'e976aa0c5dba862cfa898ea57ec226efce9d1bc04b23b8d775908db86aa6fa41',
         'https://ndownloader.figshare.com/files/51643484'),
        ('idsse_dataset/DFL_02_01_matchinformation_DFL-COM-000002_DFL-MAT-J03WR9.xml', 11823, '429b584e89df3e3e8b81f4bd0d004b38bd0b4298bb390b8fb43efccb60963e01',
         'https://ndownloader.figshare.com/files/51643490'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000001_DFL-MAT-J03WMX.xml', 776578, '6f9741ea62e9dee35b604942e1dad2ac0a4dc3fce14ef2f3858aa12b74dafe00',
         'https://ndownloader.figshare.com/files/51643493'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000001_DFL-MAT-J03WN1.xml', 612114, 'd7fa1d4445e3215eb79ec62fabefa4779b4974e496195c2fdc25624c375a9b9b',
         'https://ndownloader.figshare.com/files/51643496'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000002_DFL-MAT-J03WOH.xml', 635747, 'abc27e3268e6126fb3e6e90bff5cca8d4586a5e0cefe9bd59bf32871e89d8544',
         'https://ndownloader.figshare.com/files/51643499'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000002_DFL-MAT-J03WOY.xml', 683018, 'dbb014df1b80d5c99b7fb806a278432c445a5fdd99f59d379d601f20eaf7e142',
         'https://ndownloader.figshare.com/files/51643502'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000002_DFL-MAT-J03WPY.xml', 698898, 'e440a3adf9a38d3e4ce4289343a59a3b5f76018a78e97c765114f7817591fb3c',
         'https://ndownloader.figshare.com/files/51643505'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000002_DFL-MAT-J03WQQ.xml', 732186, 'b79ccc1ee3de5ba662546a9a21304784642d00a791ccc1175550eaa463ea0074',
         'https://ndownloader.figshare.com/files/51643508'),
        ('idsse_dataset/DFL_03_02_events_raw_DFL-COM-000002_DFL-MAT-J03WR9.xml', 681050, '31735a2d7b9008c44cae9b6ac43ab38ddeaa435d0416265ec0ebfebf53b3c982',
         'https://ndownloader.figshare.com/files/51643511'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000001_DFL-MAT-J03WMX.xml', 418524833, 'd3dd92e509421a6466acb0a083c009035f1751bc5fd9ef42ffa8f20d01cf7d49',
         'https://ndownloader.figshare.com/files/51643514'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000001_DFL-MAT-J03WN1.xml', 391722803, '56ef948961a18e150dba0b7b16869d0008ff66f3050a0c355d31fa5b8ec2fcec',
         'https://ndownloader.figshare.com/files/51643517'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000002_DFL-MAT-J03WOH.xml', 348945715, 'ec4dcf30200aad694dea263d5289485fcd0ca42badddaeb7c81f5cd5a4229d4f',
         'https://ndownloader.figshare.com/files/51643520'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000002_DFL-MAT-J03WOY.xml', 362567859, 'a228ef0e676d009cefff1580fcb721b53f598454eb120ec347e0a628a3a4646b',
         'https://ndownloader.figshare.com/files/51643523'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000002_DFL-MAT-J03WPY.xml', 371688499, '845202c29ad93d696653436da426a7cdaefb848298e07b7343de6529581671e1',
         'https://ndownloader.figshare.com/files/51643526'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000002_DFL-MAT-J03WQQ.xml', 356219423, 'cbefcb0bd7f39f3b94ee69a7bc97aac0f936425062c1cc1b144733df36804d6f',
         'https://ndownloader.figshare.com/files/51643529'),
        ('idsse_dataset/DFL_04_03_positions_raw_observed_DFL-COM-000002_DFL-MAT-J03WR9.xml', 372934140, '70b63069189019066fb7e3d9db891122edfe787f3a43ba522ebe45ed89ea0269',
         'https://ndownloader.figshare.com/files/51643532'),
    ]),
    ('SkillCorner', [
        ('skillcorner/1874553_tracking.jsonl', 90729279, 'ea97f58f8eaad925feaeacc6395ec24860dd80027af8a89450276adebd29d265',
         'https://github.com/SkillCorner/opendata/raw/refs/heads/master/data/matches/1874553/1874553_tracking_extrapolated.jsonl'),
        ('skillcorner/1886347_tracking.jsonl', 89280839, '3577e2803da95390f8b2f85d47829eb55fbbfee6211c94adc65db0dc78e46b41',
         'https://github.com/SkillCorner/opendata/raw/refs/heads/master/data/matches/1886347/1886347_tracking_extrapolated.jsonl'),
        ('skillcorner/1899585_tracking.jsonl', 85550410, '90b6289ec2181192d1793ec6240fbbe8225ff0219c7956710c6278c31a661100',
         'https://github.com/SkillCorner/opendata/raw/refs/heads/master/data/matches/1899585/1899585_tracking_extrapolated.jsonl'),
    ]),
]


# ================================================================ from fetch_public_data.py, verbatim (generated)
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download_to(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "mtah-study"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as out:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)


# ================================================================ the kit
class NetworkError(Exception):
    pass


def say(line):
    print(line, flush=True)


def matches(path, size, digest):
    return os.path.isfile(path) and os.path.getsize(path) == size and sha256(path) == digest


def remove(path):
    if os.path.exists(path):
        os.remove(path)


def get(rel, url, path, size, digest):
    """None once path holds the right file, else why not; NetworkError when the network fails."""
    part = path + ".part"
    try:
        download_to(url, part)
    except urllib.error.HTTPError as e:
        why = "not available at the source (HTTP %d)" % e.code
    except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError) as e:
        remove(part)
        raise NetworkError("%s while downloading %s" % (type(e).__name__, rel))
    else:
        if matches(part, size, digest):
            os.replace(part, path)
            return None
        why = "differs from the manifest after download"
    remove(part)
    return why


def run(out):
    lines, failed = [], []
    for name, rows in DATASETS:
        n = 0
        for rel, size, digest, url in rows:
            path = os.path.join(out, *rel.split("/"))
            why = None
            if not matches(path, size, digest):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                why = get(rel, url, path, size, digest)
            if why is None:
                n += 1
            else:
                failed.append("%s %s" % (rel, why))
        lines.append("%s %s: files %d of %d match" % (P, name, n, len(rows)))
    return lines, failed


def main(argv):
    if len(argv) != 2 or argv[0] != "--out":
        say(USAGE)
        return 2
    try:
        lines, failed = run(os.path.abspath(argv[1]))
    except NetworkError as e:                        # one line, never a traceback
        say("%s: network error (%s); check the internet connection and run again" % (P, e))
        return 1
    except OSError as e:
        say("%s: could not write in the output folder (%s)" % (P, type(e).__name__))
        return 1
    except Exception as e:
        say("%s: stopped by an unexpected error (%s)" % (P, type(e).__name__))
        return 1
    for line in lines:
        say(line)
    say("%s READY: %s" % (P, "yes" if not failed else "no (%s)" % "; ".join(failed)))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

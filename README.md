# Tiki Data: ball possession from tracking (More than a Hack 2027, phase 1)

This repository regenerates our submission file **`Tiki Data.csv`** for Barcelona 2-1 Athletic, byte for byte,
from the organisers' data bundle. It holds code only: **no match data** (see the data notice at the end).

## The method

Every frame of the tactical video gets H (the home team has the ball), A (the away team) or D (dead ball).
A players-only gradient-boosting dead-ball detector finds stoppages from how the whole field slows down, because the
ball is often missing or noisy. Where the tracked ball is shown crossing a line, the stoppage starts at that crossing.
On live frames, gradient-boosting evidence models give the log-odds that the home team has the ball. They read the
nearest players' distances to the ball and how long they stay close, the teams' shapes and pressing, contests
between the two teams' nearest players, and how the teams' runs reverse when the ball changes team, using the same
features one second later as well. The ball is first un-blurred physically wherever it is measured to be smoothed.
A three-state Viterbi decoder (home, away, dead) with a price for changing team then chooses the whole sequence at
once, so possessions do not flicker, since the ranking metric matches whole possession spells. Every model was trained
on public matches only (the DFL / IDSSE open data), never on the provided match.

The submitted version is **possession v3.1** (reference fingerprint `80f4da2a7d76d506`). The whole pipeline, its
sources and its trained models are in one generated file, `setup/possession_v3_1_standalone.py`. Before it runs, it
checks the Python version, every pinned package and the SHA-256 of every embedded source and model.
`setup/README_POSSESSION_V3_1_LEAD.txt` describes v3.1 and its risks.

## Reproduce the submission file

**Environment** (Mac or Linux, conda, the network once for the packages):

```bash
conda create -y -n tiki-data python=3.11.17
conda activate tiki-data
python -m pip install -r setup/requirements_pinned.txt
```

**The data.** Put the organisers' data bundle anywhere **outside** this repository, and set `MTAH_DATA_DIR` to the
folder that holds `tactical/`. The run reads only `tactical/BAR-ATH_tactical_atd.xml` and
`tactical/BAR-ATH_tactical_atd.txt`.

```bash
export MTAH_DATA_DIR="/path/to/the/bundle"      # the folder that holds tactical/
```

**The single command**, run from this repository's folder. It takes several minutes. The output folder must be
outside the repository; the default is `~/tiki_data_output`.

```bash
bash reproduce.sh "$MTAH_DATA_DIR" ~/tiki_data_output
```

It runs the kit, saves its screen to `~/tiki_data_output/kit_screen.txt` and compares the kit's fingerprint with
`setup/POSSESSION_V3_1_FINGERPRINT.txt`. It writes `~/tiki_data_output/Tiki Data.csv` only on a match. Expected
screen: seven `POSSESSION V3.1 KIT CHECK ...: PASS` lines, a counts line, `POSSESSION V3.1 KIT FILE: rows 199319;
validator OK`, `POSSESSION V3.1 KIT RELEASE: PASS (5 of 5)`, `POSSESSION V3.1 KIT FINGERPRINT: 80f4da2a7d76d506`,
the path of the written file, and as the **last line**:

```
V3.1 REBUILD: MATCH (80f4da2a7d76d506)
```

The fingerprint is the first 16 hex characters of the file's SHA-256. Any other last line means the file is not ours:
do not use it. (A synthetic test bundle gives another fingerprint; that is expected.)

**Then the organisers' validator** on the exact file:

```bash
git clone https://github.com/metrica-sports/more-than-a-hack-2027.git
python more-than-a-hack-2027/evaluation/validate_submission.py ~/tiki_data_output/"Tiki Data.csv"
```

It must print `OK    Tiki Data.csv` and end with `Valid.`

`setup/RUN_THIS_FIRST_v3_1.txt` is our team's step-by-step sheet for the same rebuild, kept byte-identical to the
team copy. Its steps 1 and 4 refer to the team's working repository. Here, `reproduce.sh` replaces steps 5 and 6.

## Public training data

The models were trained on public data only. To fetch it (about 2.9 GB; Python 3 standard library only):

```bash
python setup/get_public_data.py --out "/path/to/a/folder"
```

The last line must be `PUBLIC DATA READY: yes`. It downloads the 7 DFL / IDSSE matches from figshare and the 3
SkillCorner open-data matches from GitHub, and checks every file by size and SHA-256. Details and licences are in
`setup/README_PUBLIC_DATA.txt`; its notes on `code/public_data/` refer to our team's code folder. You do not need the
public data to reproduce the submission file, because the trained models are embedded in the kit.

## Before pushing a change

```bash
python3 -I tools/check_before_push.py
```

It must end with `CHECK BEFORE PUSH: PASS`. It fails on any match or data file (by name or by content), any video or
audio file, any file named after the match (`BAR-ATH`), any real-match aggregate variable, any key or token, and any
file over 50 MB. It checks both the working folder and every committed file.

## Data notice

The match data (video, audio, tracking, Smart Tagging, homography) is licensed by the organisers for this competition
only. It is **NOT in this repository** and must never be added to it. Get it from the organisers. Our output files
(`Tiki Data.csv`, `possession_v3_1.csv`, `kit_screen.txt`) are not in the repository either; `.gitignore` blocks
them, along with data folders, CSV, XML, video and audio files.

## Licence

Our code is under the MIT licence (`LICENSE`). Third-party code embedded in the kit and the public datasets we used are
credited in `THIRD_PARTY_NOTICES.md`.

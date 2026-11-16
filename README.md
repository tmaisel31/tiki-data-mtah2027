# Tiki Data FC: ball possession from tracking (More than a Hack 2027, phase 1)

## Final submission: v3.1 (team Tiki Data FC)

Our submission file is **`Tiki Data FC.csv`**, possession **v3.1**, for Barcelona 2-1 Athletic. This repository
regenerates it byte for byte from the organisers' data bundle: the reference fingerprint (the first 16 hex characters
of the file's SHA-256) is **`80f4da2a7d76d506`**. The repository holds code and documentation only, **no match data**
(see the data notice below).

### The method

Every frame of the tactical video gets H (the home team has the ball), A (the away team) or D (dead ball), from the
organisers' automatic tracking. A players-only gradient-boosting dead-ball detector finds stoppages from how the whole
field slows down, because the tracked ball is often missing or noisy; where the ball is shown crossing a line, the
stoppage starts at that crossing. On live frames, gradient-boosting evidence models give the log-odds that the home
team has the ball, from the nearest players' distances to the ball (first un-blurred physically wherever it is
measured to be smoothed) and how long they stay close, the teams' shapes and pressing, contests between the two
teams' nearest players and how the teams' runs reverse when the ball changes team, with the same features one second
later as well. A three-state Viterbi decoder (home, away, dead) with a price for changing team then chooses the whole
sequence at once, so possessions do not flicker, since the ranking metric matches whole possession spells. The models
were trained on the public DFL / IDSSE matches; no model was trained on the provided match or on its ground truth, and
the video is not an input to the pipeline.

The whole pipeline, its sources and its trained models are in one generated file,
`setup/possession_v3_1_standalone.py`. Before it runs, it checks the Python version, every pinned package and the
SHA-256 of every embedded source and model. `setup/README_POSSESSION_V3_1_LEAD.txt` describes v3.1 and its risks.

### Reproduce the submission file

Mac or Linux, with conda; the network is needed once, for the packages. Nothing is downloaded during the run itself.

**1. Clone this repository.**

```bash
git clone https://github.com/tmaisel31/tiki-data-mtah2027.git
cd tiki-data-mtah2027
```

**2. The data.** Unpack the organisers' data bundle anywhere **outside** this repository. Below, `/path/to/the/bundle`
is the folder that holds `tactical/`. The kit reads only the tracking files `tactical/BAR-ATH_tactical_atd.xml` and
`tactical/BAR-ATH_tactical_atd.txt`.

**3. The environment:** Python 3.11.17 and the exact pinned packages of `setup/requirements_pinned.txt`.

```bash
conda create -y -n tiki-v2-1 python=3.11.17
conda activate tiki-v2-1
python -m pip install -r setup/requirements_pinned.txt
```

**4. The rebuild, in one command** (several minutes). The output folder must be outside the repository; the default
is `~/tiki_data_output`.

```bash
bash reproduce.sh /path/to/the/bundle ~/tiki_data_output
```

`reproduce.sh` runs `setup/possession_v3_1_standalone.py`, saves its screen to `~/tiki_data_output/kit_screen.txt`,
and compares the fingerprint the kit prints with `setup/POSSESSION_V3_1_FINGERPRINT.txt`. Only on a match does it
write `~/tiki_data_output/Tiki Data FC.csv`. Expected screen: seven `POSSESSION V3.1 KIT CHECK ...: PASS` lines, a
counts line, `POSSESSION V3.1 KIT FILE: rows 199319; validator OK`, `POSSESSION V3.1 KIT RELEASE: PASS (5 of 5)`,
`POSSESSION V3.1 KIT FINGERPRINT: 80f4da2a7d76d506`, the path of the written file, and as the **last line**:

```
V3.1 REBUILD: MATCH (80f4da2a7d76d506)
```

Any other last line means the file is not ours: do not use it. (A synthetic test bundle gives another fingerprint;
that is expected.)

*The same rebuild step by step:* `setup/RUN_THIS_FIRST_v3_1.txt` is the team's sheet, kept byte-identical to the team's
copy, so two of its steps name the team's working repository: use step 1 above instead of its step 1, and skip its
step 4 (a check of your bundle with files kept in the team's working repository, not in this one; the fingerprint
MATCH below checks the result). Its step 2 is the environment above; step 3 checks the kit's SHA-256; step 5 is the
single command

```bash
mkdir -p ~/tiki_v3_1_output
python setup/possession_v3_1_standalone.py --data /path/to/the/bundle --out ~/tiki_v3_1_output | tee ~/tiki_v3_1_output/kit_screen.txt
```

which writes `possession_v3_1.csv` (the same bytes as `Tiki Data FC.csv`) and prints its fingerprint; step 6 compares
that fingerprint with `setup/POSSESSION_V3_1_FINGERPRINT.txt` and must print `V3.1 REBUILD: MATCH (80f4da2a7d76d506)`.

**5. The organisers' validator** on the exact file (a byte-identical copy of their `evaluation/validate_submission.py`
at commit `f8f2629`; see `evaluation/README.md`):

```bash
python evaluation/validate_submission.py ~/tiki_data_output/"Tiki Data FC.csv"
```

It must print `OK    Tiki Data FC.csv` and a line that starts with `Valid.` (the validator checks the file's format).

**Public training data (not needed to reproduce the file:** the trained models are embedded in the kit**).**
`setup/get_public_data.py` fetches the public data, 24 files, about 2.9 GB (the 7 DFL / IDSSE matches from figshare
and the 3 SkillCorner open-data matches from GitHub), and checks every file by size and SHA-256. It needs only the
Python 3 standard library:

```bash
python setup/get_public_data.py --out /path/to/a/folder
```

The last line must be `PUBLIC DATA READY: yes`. Details and licences: `setup/README_PUBLIC_DATA.txt` (its notes on
`code/public_data/` refer to the team's code folder).

## Repository map

| path | what it is |
|---|---|
| `setup/` | **the submission kit, v3.1:** `possession_v3_1_standalone.py`, `RUN_THIS_FIRST_v3_1.txt`, `POSSESSION_V3_1_FINGERPRINT.txt`, `README_POSSESSION_V3_1_LEAD.txt`, `requirements_pinned.txt`; and the public data fetcher `get_public_data.py` with `README_PUBLIC_DATA.txt` |
| `reproduce.sh` | the one-command rebuild and fingerprint check (step 4) |
| `evaluation/` | the organisers' submission validator, unchanged (MIT) |
| `tools/check_before_push.py` | the safety check run before every push (no match data, keys, home paths or files over 50 MB; last line `CHECK BEFORE PUSH: PASS`) |
| `LICENSE`, `THIRD_PARTY_NOTICES.md` | licences (below) |

## Data notice

The match data (video, audio, tracking, Smart Tagging, homography) is licensed by the organisers for this competition
only. It is **NOT in this repository** and must never be added to it; get it from the organisers. Our output files
(`Tiki Data FC.csv`, `possession_v3_1.csv`, `kit_screen.txt`) are not in the repository either. `.gitignore` blocks
them, along with data folders, CSV, XML, video and audio files, and `tools/check_before_push.py` refuses a push that
holds any of them.

## Licences

- Our code and documentation: MIT (`LICENSE`).
- The organisers' code (`evaluation/` and the files embedded in the kit): MIT, Metrica Sports (`evaluation/LICENSE`).
- Public data, not redistributed here: the DFL / IDSSE open dataset (CC BY 4.0; Bassek, Weber, Rein and Memmert,
  *Scientific Data*, 2025), used to train the models; SkillCorner open data (MIT), used for checks only; Metrica Sports
  sample data, read only to understand the provider's conventions.

Details and full credits: `THIRD_PARTY_NOTICES.md`.

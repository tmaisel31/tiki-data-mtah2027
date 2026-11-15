POSSESSION V3.1 KIT, THE LEAD VERSION (report 0410, 2026-11-11): the reference is set; how to rebuild and check it.

This file is new. It replaces the status words of README_POSSESSION_V3_1_CANDIDATE.txt (report 0409), which called
v3.1 "a PROVISIONAL CANDIDATE" with no reference fingerprint yet. That older README is a v3.1 release file and stays
unchanged. The kit itself (possession_v3_1_standalone.py) has not changed: same file, same SHA-256.

STATUS
  v3.1 is the LEAD VERSION (since 11 November 2026) and the base for all new work. It replaces v3.0 as the lead.
  Which file is uploaded as the team's submission stays the human's decision; until the human says so, the published
  submission files in Tiki-Data's setup/ are unchanged.
  Reference fingerprint: 80f4da2a7d76d506 (set by the human's first real run of v3.1, below).

HOW THE REFERENCE WAS SET (the human's runs; verdict words only)
  1. possession_v3_1.py through run_checked.sh with v3.1's screen checker: RELEASE PASS (5 of 5); GUARD FAIL, as
     v3.0's (the known graded-minute denominator effect, report 0312); POSS V3.1 SPLIT, POSS V3.1 REOPEN and
     POSS V3.1 DEAD MASK VS V2.5: WITHIN the frozen public bands; the three plausibility lines SSO CHANGE, SSO FIRED
     and SSO SECONDS: all WITHIN their frozen public bands; POSS V3.1 PLAUSIBILITY: CLEAN.
  2. release/clean_machine_test_v3_1.sh on the same data (a brand-new pinned environment): RELEASE FILES V3.1 207 of
     207 PASS, all 7 CHECK lines PASS, KIT RELEASE PASS.
  3. shasum -a 256 on possession_v3_1.py's CSV and the kit's CSV: identical (V3.1 KIT: MATCH). The kit's FINGERPRINT
     line, 80f4da2a7d76d506, is the first 16 hex characters of that SHA-256: the reference.
  4. Report 0409's frozen decision line (R1 RELEASE PASS, R2 WITHIN x3, R3 CLEAN, R4 MATCH) was met: v3.1 replaces
     v3.0 as the lead.

WHAT V3.1 IS
  v3.0 (the previous lead: v2.8-NS with the set-up mode always capped and NM16) with one change, built and chosen on
  the seven public DFL matches only:
  SSO-JOIN, the stoppage START from the ball shown out: wherever v3.0's dead mask is live while the input ball is shown
      more than 1 m beyond a goal line or touchline for at least 8 frames, the frames become dead from the crossing
      (interpolated between the last shown-inside and the first shown-outside frame) until the ball is shown back
      inside or v3.0's own stoppage begins (joined to it when it comes within 5 s; at most 20 s).
  It never re-opens a dead frame; it only turns live frames dead. Public evidence (the mean of the four deciding
  cells on the realistic noisy-ball regime RX2, against v3.0's pipeline): judge W +0.0044 on draw 2 (the deciding
  draw) and +0.0042 on draw 3; judge C +0.0039 / +0.0037; RX-REAL benches +0.0046 / +0.0051 / +0.0029 (C +0.0035 /
  +0.0042 / +0.0030). Proved SMALL-BUT-ROBUST under W and C on draws 2 and 3 (report 0409); the negative control
  failed as required and a cache-off rerun was identical. No new model; nothing trained on the provided match. The
  kit runs v3.1's configuration only (possession_v3_1.py also has OFF, which writes v3.0's file byte for byte).

RISKS
  A SMALL GAIN, NOT AN ADOPT. About +0.004 on the public cells; ADOPT's +0.008 bar was not reached, so v3.1 is in by
  the SMALL-BUT-ROBUST rule only.
  A POST HOC REPAIR. SSO-JOIN is the repair of SSO, which failed its screen (4 of 7 matches). Draw 1 designed it, so
  its deciding screen ran on fresh draw 2 (a stated deviation, frozen before any draw-2 number); draw 3 replicates.
  THROW-IN-LIKE RESTARTS. One public match (J03WN1) loses on every draw (-0.0016 to -0.0024): a firing just after a
  restart, with v3.0 already live and the ball still shown beyond the touchline (a throw-in is taken from outside the
  line). A guard for this is an untested idea.
  THE REAL BALL. The rule needs the shown ball beyond a line; how often the real ball is shown out is unknown. If it
  rarely is, v3.1 equals v3.0. The real run read SSO FIRED WITHIN its public band.
  THE PLAUSIBILITY CHECK IS COARSE: three lines against bands from public halves, read once per match. v3.1's screen
  does not print v3.0's seven SETUP / NM16 lines (v3.0 read them all WITHIN on the real match; that part is unchanged).
  CARRIED FROM V3.0: NM16 came in through the stack rule and is a bet on the written convention W; the set-up caps are
  coarse; the push-off and the blend are convention bets; the same seven public matches on every noise draw (only the
  ball noise is fresh); the END-edge caveat of report 0339; the five-minute window decides nothing; open rule
  question H3 (reports 0257, 0265).

THE FILES
  possession_v3_1_standalone.py   the whole v3.1 pipeline in one generated file (sources, with v3.0's cap table and
                                  SSO-JOIN's constants, and v2.8's models inside, each checked by SHA-256 before it
                                  runs); the team's code folder holds it as teammate_kit/possession_v3_1_standalone.py
                                  SHA-256 7ced9990555f5f7749d0c52668b2f5ae5d4203be4b6e4c154e991424498a7a12
  requirements_pinned.txt         the SAME file as for v1.9 to v3.0
                                  SHA-256 eb6136af45eae3c9281737dd28d9a0fde00c51bc353499bcd45ab195db16d78c
  POSSESSION_V3_1_FINGERPRINT.txt the team's reference, one line (written into Tiki-Data's setup/ only when the human
                                  publishes v3.1; see below):
                                  POSSESSION V3.1 KIT FINGERPRINT: 80f4da2a7d76d506

REQUIREMENTS
  As for v3.0: Mac or Linux; conda; the network once; your own copy of the match data (the folder holding
  tactical/); a few GB free; several minutes per run. The kit reads only the two tracking files.

THE STEPS
  Follow RUN_THIS_FIRST_v3_1.txt. The last command must print  V3.1 REBUILD: MATCH (80f4da2a7d76d506).

EXPECTED SCREEN OF THE KIT
  seven "POSSESSION V3.1 KIT CHECK ...: PASS" lines (python, packages, sources, model, input files, records, modules),
  one counts line "POSSESSION V3.1 KIT: possessions ...", "POSSESSION V3.1 KIT FILE: rows 199319; validator OK",
  "POSSESSION V3.1 KIT RELEASE: PASS (5 of 5)" and "POSSESSION V3.1 KIT FINGERPRINT: 80f4da2a7d76d506".

IF SOMETHING DIFFERS
  CHECK python: FAIL         the environment is not Python 3.11.17: redo step 2 of RUN_THIS_FIRST_v3_1.txt
  CHECK packages: FAIL       a package version differs: python -m pip install -r setup/requirements_pinned.txt
  CHECK sources / model      the kit file was changed or damaged: get a fresh copy and check its SHA-256 (step 3)
  CHECK input files/records  the data folder is wrong (the kit's --data is the folder ABOVE tactical) or a tracking
                             file differs: run CHECK_EVERYTHING (step 4)
  RELEASE: FAIL, or another fingerprint   the run is not the team's: do not use the file; send the team the screen
                             without the counts line
  MISMATCH (... team's: none)   setup/POSSESSION_V3_1_FINGERPRINT.txt is missing: the team has not published v3.1.
  On a fake (test) data bundle the kit prints another fingerprint (ff0ec45c317658ea on tests/fake_data.py, seed 0, the
  same as v3.0's: SSO-JOIN never fires on that bundle); that is expected and not a reference.

FOR THE HUMAN ONLY: PUBLISHING
  The kit and setup/POSSESSION_V3_1_FINGERPRINT.txt (the one line above) go into Tiki-Data's setup/ in a pull request.
  Put the fingerprint line ONLY in that file: no counts. Until then setup/ holds no v3.1 files.

SAFETY
  Never commit or upload the match data, possession_v3_1.csv or the kit's screen file (it holds the counts line) to the
  repository, an online AI tool or a cloud drive. Send files to teammates directly.

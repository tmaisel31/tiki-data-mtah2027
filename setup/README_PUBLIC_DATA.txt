PUBLIC DATA KIT: how to get our public training data on your own computer
==========================================================================

WHAT THIS IS
get_public_data.py is ONE file. It downloads, from the official sources, exactly the public data our harness and
studies read, and checks every file byte for byte (size and SHA-256) against the copies we use. It needs only Python 3
(standard library; no packages). The file was generated from our code; please do not edit it.

This is PUBLIC data, not the competition data. Nothing here comes from, or goes to, our repository.

THE DATA
1. DFL open data (the IDSSE dataset): 7 full Bundesliga and 2. Bundesliga matches (2022/23), with the position of
   every player and the ball at 25 frames per second, plus the provider's ball-status (alive/dead) and possession
   flags. For each match: the match information, the events and the positions file (21 files, 2,627,505,889
   bytes, about 2.6 GB). These are the files the floodlight library's IDSSEDataset loads for our harness.
   Source: figshare (https://ndownloader.figshare.com/files/...), as used by floodlight; the dataset is described in
   Bassek, Weber, Rein and Memmert, "An integrated dataset of spatiotemporal and event data in elite soccer",
   Scientific Data (2025), https://doi.org/10.1038/s41597-025-04505-y
   figshare record: https://doi.org/10.6084/m9.figshare.28196177.v1 (it holds exactly these 21 files).
   Licence: the figshare record's licence field reads "CC BY" with the link
   https://creativecommons.org/licenses/by/4.0/ (seen when we listed the record's files). Credit the authors.
2. SkillCorner open data: 3 A-League matches of broadcast tracking (extrapolated) with per-frame possession
   (3 files, 265,560,528 bytes, about 0.27 GB).
   Source: https://github.com/SkillCorner/opendata
   Licence: MIT License (the repository's LICENSE file, https://raw.githubusercontent.com/SkillCorner/opendata/master/LICENSE,
   first line "The MIT License")
In total 24 files, 2,893,066,417 bytes (about 2.9 GB).

THE ONE COMMAND
   python get_public_data.py --out "/path/to/a/folder"
Download time depends on your connection: about 4 minutes at 100 Mbit/s, about 20 minutes at 20 Mbit/s. The run
prints nothing while it downloads. Running it again is safe: files that are already there and correct are skipped,
so a second run downloads nothing.

WHAT THE SCREEN LINES MEAN
   PUBLIC DATA DFL: files 21 of 21 match          all 21 DFL files are there and identical to ours
   PUBLIC DATA SkillCorner: files 3 of 3 match    all 3 SkillCorner files are there and identical to ours
   PUBLIC DATA READY: yes                         everything is ready
   PUBLIC DATA READY: no (...)                    the brackets name each file that failed and why (for example
                                                  "differs from the manifest after download" or "not available at
                                                  the source (HTTP 404)"); run it again, and if it still fails,
                                                  tell the team
   PUBLIC DATA: network error (...)               the internet connection failed; nothing wrong was kept; run it
                                                  again when you are online

THE FOLDERS IT MAKES
   FOLDER/idsse_dataset/   the 21 DFL files
   FOLDER/skillcorner/     the 3 SkillCorner files

HOW TO POINT OUR SCRIPTS AT THE FOLDER
DFL (floodlight): floodlight reads the DFL files only from its own folder. Find it with
   python -c "import floodlight.settings as s; print(s.DATA_DIR)"
then link our folder into it (if an empty idsse_dataset folder is already there, remove it first):
   ln -s "/path/to/a/folder/idsse_dataset" "<that DATA_DIR>/idsse_dataset"
After this, our harness and studies load the matches without downloading anything.
SkillCorner: our fetch_public_data.py reads code/public_data/skillcorner/ and the manifest code/public_data/MANIFEST.md.
Link the folder there:
   ln -s "/path/to/a/folder/skillcorner" "code/public_data/skillcorner"
and ask the team for MANIFEST.md (a small text file of names, sizes and SHA-256; no data). Without it,
fetch_public_data.py downloads the newest SkillCorner version instead of ours.

SAFETY AND LICENCES
These are public datasets under their own licences (above): keep the credit to the sources. Do not commit the data
to our repository (code/public_data/ is in .gitignore). The kit never touches the competition data.

# Third-party notices

## 1. The organisers' code: metrica-sports/more-than-a-hack-2027 (MIT)

`setup/possession_v3_1_standalone.py` embeds, unchanged, four files of the organisers' repository
https://github.com/metrica-sports/more-than-a-hack-2027 (commit `f8f2629`). The kit checks each one's SHA-256 before
it runs:

| file in the organisers' repository | what the kit uses it for |
|---|---|
| `games.py` | the game's metadata and the paths of its input files |
| `evaluation/validate_submission.py` | validating the output file (the organisers' own checks) |
| `evaluation/possession_metrics.py` | the organisers' metric code, which the embedded modules import |
| `starter/baseline.py` | the organisers' starter loaders, which the embedded modules import |

Those files are under the organisers' MIT licence, reproduced here:

```
MIT License

Copyright (c) 2026-2027 Metrica Sports

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

As the organisers' licence states, it covers their code, documentation and public 5-minute ground truth only. It does
not cover the match data (videos, tracking, Smart Tagging, homography), which is licensed for the competition only.
None of that data is in this repository.

## 2. Training data (public; not redistributed here)

The data is not in this repository. `setup/get_public_data.py` downloads it from the official sources.

- **DFL / IDSSE open dataset**: 7 Bundesliga and 2. Bundesliga matches (2022/23), positional and event data. Licence
  CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Source: figshare,
  https://doi.org/10.6084/m9.figshare.28196177.v1. Please cite: Bassek, M., Weber, H., Rein, R. and Memmert, D.
  (2025). An integrated dataset of spatiotemporal and event data in elite soccer. *Scientific Data*.
  https://doi.org/10.1038/s41597-025-04505-y. Every embedded model was trained on these matches only.
- **SkillCorner open data**: 3 A-League matches of broadcast tracking with per-frame possession. Licence MIT
  (https://github.com/SkillCorner/opendata, LICENSE file). Used as public data for independent checks.

## 3. Python packages

The packages in `setup/requirements_pinned.txt` (for example numpy, pandas, scikit-learn, scipy and floodlight) are
installed from PyPI under their own licences. None of them is copied into this repository.

# evaluation/: the organisers' submission validator

These files are byte-identical copies from the organisers' repository
https://github.com/metrica-sports/more-than-a-hack-2027 at commit
`f8f2629ff1e0985f81d7e59d8413678514ee1530`, under their MIT licence (`LICENSE` here, with the organisers' scope note):

| file here | path in the organisers' repository | SHA-256 |
|---|---|---|
| `validate_submission.py` | `evaluation/validate_submission.py` | `07ac29499acbd337e1dc1de1832d63f6e1fa1d981e22f6ad08212529e2bbee14` |
| `possession_metrics.py` | `evaluation/possession_metrics.py` | `341bad48904b489d6e875397b27687f5d6a4d22a397f3dc8af3a00d48f16874d` |
| `games.py` | `games.py` | `3b2122794e9e0476e2b3a871d14880e5fa47c4feaeacf99caef054c2309076ce` |
| `LICENSE` | `LICENSE` | `b1f93728571a232a0e158abdd869891f2efd51894134fb20678292c2468ff3ec` |

`validate_submission.py` imports `possession_metrics` and `games`, and looks for them in its own folder first, so
`games.py` sits here instead of one folder up as in the organisers' layout. Nothing in these files reads the match
data. Run it on the rebuilt file (it needs numpy and pandas, both in `setup/requirements_pinned.txt`):

```bash
python evaluation/validate_submission.py ~/tiki_data_output/"Tiki Data FC.csv"
```

It must print `OK    Tiki Data FC.csv`.

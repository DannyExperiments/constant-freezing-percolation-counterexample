# Reproduce the checks

Run from the repository root with Python 3.11 or newer:

```sh
python3 scripts/verify_repository.py
python3 verification/src/replay.py
```

The replay uses the standard library and exact rational arithmetic. It verifies the identity at 63 rational rates, the exact sign bracket, a negative rational covariance at $\alpha=1/1000$, and all eight masses for Mottram’s four-vertex path at $\alpha=1$. See the [saved output](verification/logs/replay.txt). The proof of the degree bound appears in the [manuscript](paper/manuscript.pdf).

See the [PDF build guide](paper/BUILD.md) and [illustration rebuild guide](visualization/README.md) for those artifacts.

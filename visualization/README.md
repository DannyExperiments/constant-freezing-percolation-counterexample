# Worked illustration

The rotating tetrahedron displays three exact families of jump histories from the proof. Gold marks a closed edge of $M=\{01,23\}$. Pale lines mark closed cross edges, green lines are open edges, and dashed lines are blocked. Blue vertices are frozen.

Extract [the explorer ZIP](freezing-histories-explorer.zip) and open `index.html` in a browser. Select a history, use the Previous and Next jump buttons, and rotate with the slider or a pointer drag. Each representative drawing displays the symmetry-counted next jump factor. The explorer runs offline.

To regenerate both downloads, use Python 3.11+ with Pillow and a local DejaVu Sans font pair. From the repository root run

```sh
python3 visualization/render.py --fonts /path/to/dejavu-font-directory
```

The generator reads the explorer’s jump fixtures and checks all moves, state counts, terminal consequences and grouped history probabilities against the exact replay at $\alpha=1/1000$. At the reference settings, Pillow 13.0.0 renders a 704 × 760 GIF with 33 frames over 21 seconds.

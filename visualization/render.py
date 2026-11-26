"""Render the GIF and offline explorer ZIP, using the exact replay to check all histories."""

import argparse
from fractions import Fraction
from functools import cache
import json
from math import cos, sin
from pathlib import Path
import re
import runpy
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
W, H = 704, 760
POINTS = ((-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))
BG, CARD, INK, MUTED = "#081423", "#122237", "#f5f3eb", "#acbccc"
GOLD, GREEN, BLUE, SLATE = "#ffc670", "#6de4b2", "#83c6ff", "#63798e"
BORDER = "#30445a"


def read_histories():
    page = (HERE / "index.html").read_text(encoding="utf-8")
    return json.loads(re.search(r'<script type="application/json" id="histories">(.*?)</script>', page, re.S)[1])


def check_histories(histories):
    model = runpy.run_path(str(HERE.parent / "verification/src/replay.py"))
    edges = model["COMPLETE"]
    matching = model["MATCHING_MASK"]
    cross = model["OTHER_MASK"]
    alpha = Fraction(1, 1000)
    law = model["final_law"](edges, alpha)
    empty = law[0]
    miss_m = sum(mass for opened, mass in law.items() if not opened & matching)
    miss_c = sum(mass for opened, mass in law.items() if not opened & cross)
    expected_families = [
        [(6, 4, 4), (3, 3, 3), (1, 2, 2)],
        [(6, 4, 4), (5, 3, 1)],
        [(6, 4, 2), (5, 3, 1), (4, 2, 2)],
    ]
    outputs = []
    for scene, history in enumerate(histories):
        opened = frozen = 0
        stages = [(opened, frozen, None)]
        actual_sizes = []
        mass = Fraction(1)
        for jump in history["steps"]:
            live, parts = model["exits"](edges, opened, frozen)
            cardinality = jump["choices"]
            actual_sizes.append((len(live), len(parts), cardinality))
            if jump["op"] == "open":
                index = edges.index(tuple(jump["vertices"]))
                assert index in live
                opened |= 1 << index
                numerator = cardinality
                factor = str(cardinality)
            else:
                mask = sum(1 << v for v in jump["vertices"])
                assert mask in parts
                frozen |= mask
                numerator = cardinality * alpha
                factor = ("α" if cardinality == 1 else f"{cardinality}α")
            j, k = len(live), len(parts)
            mass *= numerator / (j + k * alpha)
            stages.append((opened, frozen, f"{factor} / ({j} + {k}α)"))
        assert actual_sizes == expected_families[scene]
        remaining, _ = model["exits"](edges, opened, frozen)
        still_possible = opened | sum(1 << i for i in remaining)
        excluded_mask = (matching | cross, matching, cross)[scene]
        assert not still_possible & excluded_mask
        assert (mass == empty, mass <= miss_m, mass <= miss_c)[scene]
        outputs.append((history, stages))
    assert empty < miss_m * miss_c
    return edges, matching, outputs


def dashed(draw, start, end, fill, width):
    x0, y0 = start
    dx, dy = end[0] - x0, end[1] - y0
    length = (dx*dx + dy*dy)**.5
    if length < 1:
        return
    for offset in range(0, int(length), 21):
        begin, finish = offset / length, min(length, offset + 11) / length
        draw.line((x0 + begin*dx, y0 + begin*dy, x0 + finish*dx, y0 + finish*dy), fill, width)


def project(angle):
    elevation = .43
    result = []
    for x, y, z in POINTS:
        x1, z1 = cos(angle)*x + sin(angle)*z, cos(angle)*z - sin(angle)*x
        y1 = cos(elevation)*y - sin(elevation)*z1
        depth = sin(elevation)*y + cos(elevation)*z1
        lens = 5.2 / (5.2 - depth)
        result.append((352 + x1*lens*101, 305 - y1*lens*101, depth))
    return result


def draw_graph(draw, angle, edges, matching, opened, frozen, fonts):
    coords = project(angle)
    depth = lambda ei: sum(coords[v][2] for v in edges[ei])
    for index in sorted(range(len(edges)), key=depth):
        u, v = edges[index]
        points = (coords[u][:2], coords[v][:2])
        if opened & (1 << index):
            draw.line(points, GREEN, 13)
        elif frozen & ((1 << u) | (1 << v)):
            dashed(draw, *points, SLATE, 4)
        elif matching & (1 << index):
            draw.line(points, GOLD, 8)
        else:
            draw.line(points, MUTED, 5)
    for vertex in sorted(range(4), key=lambda index: coords[index][2]):
        x, y, _ = coords[vertex]
        color = BLUE if frozen & (1 << vertex) else INK
        draw.ellipse((x-21, y-21, x+21, y+21), fill=color, outline=BG, width=3)
        draw.text((x, y), str(vertex), fill=BG, font=fonts(25, True), anchor="mm")


def render_frame(scene, step, offset, history, stages, edges, matching, fonts):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    def text(x, y, label, size, color=INK, bold=False):
        font = fonts(size, bold)
        assert draw.textlength(label, font=font) + x <= W-31, label
        draw.text((x, y), label, color, font=font, anchor="lt")

    opened, frozen, factor = stages[step]
    text(35, 29, "CONSTANT-FREEZING PERCOLATION", 22, MUTED, True)
    text(35, 67, history["title"], 48, INK, True)
    draw.rounded_rectangle((30, 137, 674, 505), radius=20, fill=CARD, outline=BORDER, width=2)
    draw_graph(draw, .74 + .075 * (step+offset), edges, matching, opened, frozen, fonts)
    for x, label, color in ((55, "M edge", GOLD), (192, "Open", GREEN), (312, "Blocked", MUTED), (462, "Frozen vertex", BLUE)):
        text(x, 465, label, 21, color, True)
    text(35, 524, f"HISTORY {scene+1}/3   ·   JUMP {step}/{len(history['steps'])}", 22, MUTED, True)
    title = "All edges start closed" if not step else history["steps"][step-1]["label"]
    text(35, 567, title, 39, INK, True)
    detail = "M = {01, 23}   ·   C = other edges" if not step else f"Jump factor   {factor}"
    text(35, 624, detail, 29, GOLD, True)
    draw.line((35, 679, 669, 679), BORDER, width=2)
    finish = step == len(history["steps"])
    text(35, 704, history["short"] if finish else "Open an edge or freeze a warm component", 26, GREEN if finish else MUTED, finish)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonts", type=Path, required=True, help="Directory with DejaVuSans.ttf and DejaVuSans-Bold.ttf")
    parser.add_argument("--output", type=Path, default=HERE)
    args = parser.parse_args()

    @cache
    def fonts(size, bold=False):
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(str(args.fonts / name), size)

    edges, matching, outputs = check_histories(read_histories())
    frames = []
    durations = []
    for scene, (history, stages) in enumerate(outputs):
        for step in range(len(stages)):
            for offset in range(3):
                frame = render_frame(scene, step, offset/3, history, stages, edges, matching, fonts)
                frames.append(frame.quantize(colors=64, dither=Image.Dither.NONE))
                durations.append(100 if offset < 2 else (2400 if step == len(stages) - 1 else 1450))
    args.output.mkdir(parents=True, exist_ok=True)
    frames[0].save(args.output / "freezing-histories.gif", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=1, optimize=True)
    entry = ZipInfo("index.html", date_time=(2026, 11, 26, 0, 0, 0))
    entry.create_system = 3
    entry.external_attr = 0o100644 << 16
    with ZipFile(args.output / "freezing-histories-explorer.zip", "w") as archive:
        archive.writestr(entry, (HERE / "index.html").read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
    print(f"Checked three history families and wrote {len(frames)} frames ({W} × {H}, {sum(durations)/1000:g} s).")


if __name__ == "__main__":
    main()

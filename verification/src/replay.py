"""Exact forward-flow certificate and Mottram's four-vertex path calibration."""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations


VERTICES = range(4)
FULL_VERTEX_MASK = (1 << len(VERTICES)) - 1
COMPLETE = tuple(combinations(VERTICES, 2))
PATH = ((0, 1), (1, 2), (2, 3))
MATCHING_MASK = (1 << COMPLETE.index((0, 1))) | (1 << COMPLETE.index((2, 3)))
OTHER_MASK = ((1 << len(COMPLETE)) - 1) ^ MATCHING_MASK
COEFFICIENTS = (-594, 9744, 101962, 371058, 712884, 820280,
                593838, 272838, 77334, 12384, 864)


def exits(edges, opened, frozen):
    """Return indices of eligible edges and masks of warm components."""
    live = []
    blocks = [1 << i for i in VERTICES if not (frozen & (1 << i))]
    for index, (u, v) in enumerate(edges):
        endpoints = (1 << u) | (1 << v)
        if frozen & endpoints:
            continue
        if not (opened & (1 << index)):
            live.append(index)
            continue
        merged = 0
        remaining = []
        for block in blocks:
            if block & endpoints:
                merged |= block
            else:
                remaining.append(block)
        blocks = remaining + [merged]
    return live, blocks


def final_law(edges, alpha, *, check_strict_edge_decrease=False):
    """The rank counts opened edges and frozen vertices and increases at each jump."""
    assert alpha > 0
    levels = [defaultdict(Fraction) for _ in range(len(edges) + len(VERTICES) + 1)]
    levels[0][0, 0] = Fraction(1)
    terminal = defaultdict(Fraction)
    for rank, states in enumerate(levels):
        for (opened, frozen), mass in states.items():
            assert opened.bit_count() + frozen.bit_count() == rank
            assert frozen <= FULL_VERTEX_MASK and mass > 0
            live, warm_blocks = exits(edges, opened, frozen)
            if not live:
                terminal[opened] += mass
                continue
            total_rate = len(live) + alpha * len(warm_blocks)
            opening_mass = mass / total_rate
            for index in live:
                next_opened = opened | (1 << index)
                if check_strict_edge_decrease:
                    assert len(exits(edges, next_opened, frozen)[0]) < len(live)
                levels[rank + 1][next_opened, frozen] += opening_mass
            for block in warm_blocks:
                next_frozen = frozen | block
                if check_strict_edge_decrease:
                    assert len(exits(edges, opened, next_frozen)[0]) < len(live)
                levels[rank + block.bit_count()][opened, next_frozen] += alpha * opening_mass
    assert sum(terminal.values()) == 1
    return terminal


def covariance(law):
    miss_m = sum(mass for edges, mass in law.items() if not (edges & MATCHING_MASK))
    miss_c = sum(mass for edges, mass in law.items() if not (edges & OTHER_MASK))
    return law[0] - miss_m * miss_c


def polynomial(alpha):
    value = Fraction(0)
    for coefficient in reversed(COEFFICIENTS):
        value = alpha * value + coefficient
    return value


def formula(x):
    denominator = 9 * (1 + 2*x)**2 * (1 + x)**5 * (3 + 2*x)**2 * (2 + x)**3 * (5 + 3*x)**2
    return x**2 * polynomial(x) / denominator


def certify_identity():
    # K4's strict eligible-edge decrease gives a common denominator for each
    # event of degree 24, hence a covariance numerator of degree at most 48.
    # Cross-multiplication by the degree-14 target denominator gives degree 62.
    for i in range(1, 64):
        x = Fraction(i, 1000)
        law = final_law(COMPLETE, x, check_strict_edge_decrease=True)
        assert len(law) == 64
        assert covariance(law) == formula(x), f"rational identity fails at {x}"
    print("Rational identity: 63 distinct exact values, cleared degree at most 62.")


def check_path_calibration():
    law = final_law(PATH, Fraction(1))
    # Bit order is 01, 12, 23. Mottram's common denominator at alpha=1 is 105.
    assert [law[i] for i in range(8)] == [Fraction(m, 105) for m in (34, 15, 13, 8, 15, 6, 8, 6)]
    lattice_defect = law[0b101] * law[0b000] - law[0b001] * law[0b100]
    assert lattice_defect == -Fraction(1, 525)
    print("P4 at alpha = 1: eight masses agree with the thesis; lattice defect = -1/525.")


def main():
    certify_identity()
    lower = Fraction(407722920, 10**10)
    upper = Fraction(407722921, 10**10)
    assert COEFFICIENTS[0] < 0 and all(value > 0 for value in COEFFICIENTS[1:])
    assert polynomial(lower) < 0 < polynomial(upper)
    print("The unique positive root is between 0.0407722920 and 0.0407722921.")
    alpha = Fraction(1, 1000)
    law = final_law(COMPLETE, alpha, check_strict_edge_decrease=True)
    assert law[0] == Fraction(1, 752753001)
    assert covariance(law) < 0
    print(f"K4 at alpha = 1/1000: exact covariance = {covariance(law)}.")
    check_path_calibration()


if __name__ == "__main__":
    main()

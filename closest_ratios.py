#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Brute force method for working on the problem of finding the closest possible value for
two ratios between 0 and 1, given a specified maximum denominator.  The open question is
whether the closest ratios are ever *not* at the extremities--that is, neither the lowest
nor highest constructable ratios (``1/max_denom`` or ``(max_denom-1)/max_denom``) are
involved.
"""

import sys

# high water mark (representation must be contiguous below)
hi_denom = 2
# map of ratio value to (num, denom) tuple
operands: dict[float, tuple[int, int]] = {}
# list of ratio values, always sorted in-place for faster resorts
ratios: list[float] = []

def closest_ratios(max_denom: int, mid_pack: bool = False) -> None:
    """Find closest, non-identical ratios with denominator less than `max_denom`.  If
    `mid_pack` is specified as True, then skip computing the ratios at the extremities
    (i.e. where numerator is either 1 or `denom - 1`).

    Return tuple of (ratio1, ratio2, diff, is_mid), where the two ratios are represented
    as tuple of (num, denom), and is_mid indicates whether the result is one of the two
    extremity cases.

    Note that this problem space is symmetrical around a midpoint (of numerator domain):
    every pair of ratios, `(n1/d1)` and `(n2/d2)`, has a companion pair, `((d1-n1)/d1)`
    and `((d2-n2)/d2)`, with an identical difference.  Thus, we only need to explore the
    first half of possible numerators for any given denominator (none of the differences
    we are interested in spans the two halfs of the domain).
    """
    global operands, ratios, hi_denom
    assert max_denom > (4 if mid_pack else 2), "Degenerate case"
    assert max_denom > hi_denom, "Calling out of order"

    for denom in range(hi_denom, max_denom + 1):
        # we only have to run through the first half of possible numerators, since the
        # problem space is symmetrical around the midpoint
        for num in range(2 if mid_pack else 1, denom // 2 + 1):
            val = num / denom
            # only record the first encounter
            if val not in operands:
                operands[val] = (num, denom)
                ratios.append(val)
    hi_denom = max_denom

    ratios.sort()
    min_pair = None
    min_diff = 1.0
    prev_val = 0.0
    for val in ratios:
        if val - prev_val < min_diff:
            min_diff = val - prev_val
            min_pair = (prev_val, val)
        prev_val = val

    ratio1 = operands[min_pair[0]]
    ratio2 = operands[min_pair[1]]
    # we can do this by checking the appropriate numerators
    is_mid = ratio1[0] != 1 and ratio2[0] != max_denom - 1
    return ratio1, ratio2, min_diff, is_mid

def prt_info(diff_info: tuple | None, scope: str) -> None:
    """Little utility function for printing encapsulated info for close ratio pairs
    (called from main)
    """
    as_str = lambda x: f"{x[0]}/{x[1]}"
    if diff_info is None:
        print(f"\nNo {scope} closest ratios found")
        return
    n, ratio1, ratio2, diff, is_mid = diff_info
    print(f"\nClosest {scope} ratios found:"
          f"\nFor max denom {n}: {as_str(ratio1)} and {as_str(ratio2)}, diff = {diff:.12f}")

def main() -> int:
    """Usage: python -m closest_ratios <max_denom> [<mid_pack> [<trace>]]

    where:

    - ``mid_pack`` (bool) - indicates whether to ignore ratios at the extremities (noting
      that a midpack closest ratio pair will always be reported if found, regardless)
    - ``trace`` (bool) - indicates whether to trace progress during the run
    """
    bool_val = lambda x: len(x) > 0 and x[0].lower() not in ('0', 'n', 'f')
    mid_pack = False
    trace = False
    if len(sys.argv) < 2:
        print(f"Missing arg(s)\n\n{main.__doc__}")
        return 1
    max_denom = int(sys.argv[1])
    if len(sys.argv) > 2:
        mid_pack = bool_val(sys.argv[2])
        if len(sys.argv) > 3:
            trace = bool_val(sys.argv[3])

    # index: 0 - overall, 1 - midpack
    min_diff = [1.0, 1.0]
    min_diff_info = [None, None]
    start_denom = 5 if mid_pack else 3
    try:
        for n in range(start_denom, max_denom + 1):
            ratio1, ratio2, diff, is_mid = closest_ratios(n, mid_pack)
            trace and print(f"{n}: {ratio1}, {ratio2}, {diff:.12f}, {is_mid}")
            if diff < min_diff[0]:
                min_diff[0] = diff
                min_diff_info[0] = (n, ratio1, ratio2, diff, is_mid)
            if is_mid and diff < min_diff[1]:
                min_diff[1] = diff
                min_diff_info[1] = (n, ratio1, ratio2, diff, is_mid)
    except KeyboardInterrupt:
        print(f"Interrupted after {n - start_denom} loops...")

    if not mid_pack:
        prt_info(min_diff_info[0], "overall")
    prt_info(min_diff_info[1], "midpack")
    return 0

if __name__ == "__main__":
    sys.exit(main())

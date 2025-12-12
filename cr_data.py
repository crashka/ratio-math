#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to generate CSV data from ``closest_ratio``.

Usage: python -m cr_data <max_denom>

Output fields:

- max_denom
- mp_diff
- extrm_diff
- mp_ratio1_num
- mp_ratio1_denom
- mp_ratio2_num,
- mp_ratio2_denom
"""

import sys

from closest_ratios import closest_ratios

"""Notes:

Need to support graphical representation of the following:

- Best midpack solution (ratio closeness)
- Diff of best midpack solution to extremity solution
- Ratio for best midpack solution (average of close ratio pair)
"""
if len(sys.argv) < 2:
    sys.exit(f"Missing arg(s)\n\n{__doc__}")
max_denom = int(sys.argv[1])

fields = ("max_denom", "mp_diff", "extrm_diff", "mp_ratio1_num", "mp_ratio1_denom",
          "mp_ratio2_num", "mp_ratio2_denom")
print(','.join(fields))

start_denom = 5
for n in range(start_denom, max_denom + 1):
    mp_ratio1, mp_ratio2, mp_diff, is_mid = closest_ratios(n, midpack=True)
    extrm_diff = (1 / (n - 1)) - (1 / n)
    data = (n, mp_diff, extrm_diff, *mp_ratio1, *mp_ratio2)
    print(','.join(map(str, data)))

#!/usr/bin/env python
# import numpy as np
import re
import sys


def look_around_stars(L):
    sum_gear_ratio = 0
    for i, s in enumerate(L):
        for j, c in enumerate(s[:-1]):
            if c == "*":
                sum_gear_ratio += look_around_loc(L, i, j)
    return sum_gear_ratio


def look_around_loc(L, i, j):
    parts = []
    if i > 0:
        parts.extend(scan_row(L[i - 1], j))
    parts.extend(scan_row(L[i], j))
    if i < len(L) - 1:
        parts.extend(scan_row(L[i + 1], j))
    if len(parts) == 2:
        return parts[0] * parts[1]
    else:
        return 0


def scan_row(s, j):
    parts = []
    if re.search(r"\d", s[min(0, j - 1) : max(len(s), j + 1 + 1)]):
        for m in re.finditer(r"(\d+)", s):
            if m.start() > j + 1:
                break
            elif m.start() <= j + 1 and m.end() > j - 1:
                parts.append(int(m.group()))
    return parts


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
        print(look_around_stars(L))


if __name__ == "__main__":
    sys.exit(main())

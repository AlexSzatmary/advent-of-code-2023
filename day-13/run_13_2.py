#!/usr/bin/env python
import timeit
import numpy as np
import sys


def parse_input(L):
    L.append("\n")
    patterns = []
    pattern_raw = []
    for s in L:
        if s == "\n":
            patterns.append(np.array(pattern_raw))
            pattern_raw = []
        else:
            pattern_raw.append([1 if c == "#" else 0 for c in s[:-1]])
    return patterns


def scan_rows(pattern):
    m = np.size(pattern, 0)

    def off_by_one(a, b):
        return np.sum(np.abs(a - b)) == 1

    for r in range(1, m // 2 + 1):
        # print(r, m)
        if off_by_one(pattern[:r], pattern[2 * r - 1 : r - 1 : -1]):
            return r
    for r in range(m // 2 + 1, m):
        # print(r, m)
        if off_by_one(pattern[2 * r - m:r], pattern[-1: r - 1 : -1]):
            return r
    return 0


def scan_cols(pattern):
    return scan_rows(pattern.T)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    patterns = parse_input(L)
    total = 0
    for i, pattern in enumerate(patterns):
        summary = scan_cols(pattern) + 100 * scan_rows(pattern)
        total += summary
        print(i, summary, total)
    print("Total: ", total)
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

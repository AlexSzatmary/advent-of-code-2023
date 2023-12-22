#!/usr/bin/env python
import numpy as np
import sys


def parse_input(L):
    a = np.array([[1 if c == "#" else 0 for c in s[:-1]] for s in L])
    rs, cs = np.where(a)
    hspace = np.cumsum(1 - np.max(a, 0))
    vspace = np.cumsum(1 - np.max(a, 1))
    return a, rs, cs, hspace, vspace


def distance(ra, ca, rb, cb, hspace, vspace):
    return (
        abs(ra - rb)
        + abs(vspace[ra] - vspace[rb]) * 999_999
        + abs(ca - cb)
        + abs(hspace[ca] - hspace[cb]) * 999_999
    )


def add_distances(rs, cs, hspace, vspace):
    dtot = 0
    for i in range(len(rs) - 1):
        for j in range(i + 1, len(rs)):
            dtot += distance(rs[i], cs[i], rs[j], cs[j], hspace, vspace)
    return dtot


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    a, rs, cs, hspace, vspace = parse_input(L)
    print(add_distances(rs, cs, hspace, vspace))


if __name__ == "__main__":
    sys.exit(main())

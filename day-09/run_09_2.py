#!/usr/bin/env python
# from itertools import cycle
import re
import sys


def parse_input(L):
    rows = []
    for s in L:
        rows.append(list(map(int, re.findall(r"(-?\d+)", s))))
    return rows


def predict(row):
    row = list(reversed(row))
    print(row)
    tableau = []
    tableau.append([row[i + 1] - row[i] for i in range(len(row) - 1)])
    while not all(x == 0 for x in tableau[-1]):
        r = tableau[-1]
        tableau.append([r[i + 1] - r[i] for i in range(len(r) - 1)])
    lower_end = 0
    for r in reversed(tableau):
        lower_end += r[-1]
    return row[-1] + lower_end


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    rows = parse_input(L)
    print(sum(map(predict, rows)))


if __name__ == "__main__":
    sys.exit(main())

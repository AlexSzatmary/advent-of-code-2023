#!/usr/bin/env python
# import numpy as np
import re
import sys


def process_line(s):
    (winners, mine) = [
        [int(m) for m in re.findall(r"\d+", group)]
        for group in re.search(r": ([^|]*) \| (.*)", s).groups()
    ]
    return int(2 ** (len(set(winners).intersection(set(mine))) - 1))


def add_lines(L):
    return sum(process_line(s) for s in L)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
        print(add_lines(L))


if __name__ == "__main__":
    sys.exit(main())

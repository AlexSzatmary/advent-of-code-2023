#!/usr/bin/env python
# import numpy as np
import numpy as np
import re
import sys


def process_line(s):
    (winners, mine) = [
        [int(m) for m in re.findall(r"\d+", group)]
        for group in re.search(r": ([^|]*) \| (.*)", s).groups()
    ]
    return len(set(winners).intersection(set(mine)))


def add_lines(L):
    wins = np.ones(len(L))
    for i, s in enumerate(L):
        wins[i + 1:i + process_line(s) + 1] += wins[i]
    return sum(wins)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
        print(add_lines(L))


if __name__ == "__main__":
    sys.exit(main())

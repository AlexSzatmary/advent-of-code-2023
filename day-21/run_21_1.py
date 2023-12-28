#!/usr/bin/env python
import numpy as np
import timeit
import sys


def parse_input(L):
    # Zero pad array; only +1 is added to the string length because we want to drop the
    # newline anyway
    field = np.ones((len(L) + 2, len(L[0]) + 1), dtype=np.int_)
    for i, s in enumerate(L):
        if (j := s.find("S")) != -1:
            starti = i + 1
            startj = j + 1
            s = s.replace("S", "0")
        field[i + 1, 1:-1] = np.array(
            list(s[:-1].replace(".", "0").replace("#", "1")), dtype=np.int_
        )
    return starti, startj, field


def walk(starti, startj, field, n):
    walked = np.zeros(np.shape(field), dtype=np.int_)
    walked[starti, startj] = 1
    for k in range(n):
        walked[1:-1, 1:-1] = (1 - field[1:-1, 1:-1]) * (
            [
                walked[0:-2, 1:-1]
                | walked[2:, 1:-1]
                | walked[1:-1, 0:-2]
                | walked[1:-1, 2:]
            ]
        )
    return walked


def print_field_and_walked(field, walked):
    for i in range(len(field)):
        print(
            "".join(
                "#" if f else ("O" if w else ".")
                for f, w in zip(field[i, :], walked[i, :])
            )
        )


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    starti, startj, field = parse_input(L)
    walked = walk(starti, startj, field, 64)
    print_field_and_walked(field, walked)
    print(starti, startj)
    print(np.sum(walked > 0))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

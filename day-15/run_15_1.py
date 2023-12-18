#!/usr/bin/env python
# from itertools import cycle
import timeit
import sys


def parse_input(L):
    return L[0].split(",")


def h(s):
    a = 0
    for c in s:
        a = (a + ord(c)) * 17 % 256
    return a


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    steps = parse_input(L)
    print(sum(map(h, steps)))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
from itertools import cycle
import re
import sys


def parse_input(L):
    instructions = L[0][:-1]
    network = {}
    for s in L[2:]:
        node, left, right = re.match(r"(\w+)\W+(\w+)\W+(\w+)", s).groups()
        network[node] = (left, right)
    return instructions, network


def roam(instructions, network):
    here = "AAA"
    c = 0
    instructions = cycle(instructions)
    while here != "ZZZ":
        here = network[here][0 if next(instructions) == "L" else 1]
        c += 1
    return c


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    instructions, network = parse_input(L)
    # print(instructions)
    # print(network)
    distance = roam(instructions, network)
    print(distance)


if __name__ == "__main__":
    sys.exit(main())

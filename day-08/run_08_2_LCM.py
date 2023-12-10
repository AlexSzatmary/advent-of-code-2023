#!/usr/bin/env python
from itertools import cycle
import math
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
    ghosts = [node for node in network if node[-1] == "A"]
    # print(ghosts)
    c = 0
    instructions = cycle(instructions)
    while any([ghost[-1] != "Z" for ghost in ghosts]):
        instruction = next(instructions)
        next_ghosts = [
            network[ghost][0 if instruction == "L" else 1] for ghost in ghosts
        ]
        ghosts = next_ghosts
        c += 1
    return c


def roam_LCM(instructions, network):
    ghosts = [node for node in network if node[-1] == "A"]
    return [roam_LCM_ghost(instructions, network, ghost) for ghost in ghosts]


def roam_LCM_ghost(instructions, network, ghost):
    c = 0
    div = len(instructions)
    instructions = cycle(instructions)
    while c % div or ghost[-1] != "Z":
        ghost = network[ghost][0 if next(instructions) == "L" else 1]
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
    distances = roam_LCM(instructions, network)
    print(math.lcm(*distances))


if __name__ == "__main__":
    sys.exit(main())

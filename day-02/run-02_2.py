#!/usr/bin/env python
import re
import sys


def sum_game_power(L):
    power = 0
    comma_semicolon = re.compile("[,;]")
    for s in L:
        rest = s.split(":")[1]
        nr = ng = nb = 0
        for observation in comma_semicolon.split(rest):
            n, cube = observation[1:].split()
            n = int(n)
            match cube[0]:
                case "r":
                    nr = max(n, nr)
                case "g":
                    ng = max(n, ng)
                case "b":
                    nb = max(n, nb)
        power += nr * ng * nb
    return power


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1]) as hin:
        L = hin.readlines()
    print(sum_game_power(L))


if __name__ == "__main__":
    sys.exit(main())

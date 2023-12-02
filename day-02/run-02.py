#!/usr/bin/env python
import re
import sys

LIMIT = {"r": 12, "g": 13, "b": 14}


def sum_game_impossible_ids(L):
    sum_ids = 0
    comma_semicolon = re.compile("[,;]")
    for s in L:
        game_i, rest = s.split(":")
        for observation in comma_semicolon.split(rest):
            n, cube = observation[1:].split()
            if int(n) > LIMIT[cube[0]]:
                break
        else:
            sum_ids += int(game_i.split()[1])
    return sum_ids


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1]) as hin:
        L = hin.readlines()
    print(sum_game_impossible_ids(L))


if __name__ == "__main__":
    sys.exit(main())

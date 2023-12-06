#!/usr/bin/env python
import re
import sys


def parse_tables(L):
    seeds = list(map(int, re.findall(r"\d+", L[0])))
    maps = []
    map_names = []
    for s in L[1:]:
        if m := re.match(r"(.*):", s):
            map_names.append(m.group(1))
            maps.append([])
        elif m := re.match(r"(\d+) (\d+) (\d+)", s):
            maps[-1].append(tuple(map(int, m.groups())))
        else:
            pass
    return seeds, map_names, maps


def apply_map(i, m):
    for dest, src, length in m:
        if src <= i < src + length:
            return i - src + dest
    return i


def apply_all_maps(seed, maps):
    i = seed
    for m in maps:
        i = apply_map(i, m)
    return i


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
        seeds, map_names, maps = parse_tables(L)
        locs = [apply_all_maps(seed, maps) for seed in seeds]
        print(min(locs))


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
# import itertools
import re
import sys


def parse_tables(L):
    seeds = [tuple(map(int, x)) for x in re.findall(r"(\d+) (\d+)", L[0])]
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
    # map_ is a map in the context of the problem, not map()
    for map_ in maps:
        map_.sort(key=lambda entry: entry[1])
    return seeds, map_names, maps


def apply_map(in_start, in_length, map_):
    # map_ is a map in the context of the problem, not map()
    out_starts = []
    out_lengths = []
    for dest, src, length in map_:
        if in_start < src + length:
            if in_start + in_length < src + length:
                if in_start + in_length < src:
                    out_starts.append(in_start)
                    out_lengths.append(in_length)
                elif in_start < src:
                    out_starts.append(in_start)
                    out_lengths.append(src - in_start)
                    out_starts.append(dest)
                    out_lengths.append(in_start + in_length - src)
                else:  # src < in_start
                    out_starts.append(dest + in_start - src)
                    out_lengths.append(in_length)
                return out_starts, out_lengths
            else:  # span not consumed
                if in_start < src:
                    out_starts.append(in_start)
                    out_lengths.append(src - in_start)
                    out_starts.append(dest)
                    out_lengths.append(length)
                else:
                    out_starts.append(in_start + dest - src)
                    out_lengths.append(src + length - in_start)
                in_start, in_length = src + length, in_start + in_length - src - length
    out_starts.append(in_start)
    out_lengths.append(in_length)
    return out_starts, out_lengths


def apply_all_maps(seed, maps):
    in_start, in_length = seed
    in_starts = [in_start]
    in_lengths = [in_length]
    for map_ in maps:
        in_starts_new = []
        in_lengths_new = []
        for in_start, in_length in zip(in_starts, in_lengths):
            out_starts, out_lengths = apply_map(in_start, in_length, map_)
            in_starts_new.extend(out_starts)
            in_lengths_new.extend(out_lengths)
        in_starts = in_starts_new
        in_lengths = in_lengths_new
    return in_starts_new, in_lengths_new


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    seeds, map_names, maps = parse_tables(L)
    starts = []
    for seed in seeds:
        start, length = apply_all_maps(seed, maps)
        starts.extend(start)
    print(min(starts))        


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
from functools import cache
import timeit
import re
import sys


def parse_input(L):
    rows = []
    for s in L:
        row, groups = s.split(" ")
        repeats = 5
        row = "?".join(row for i in range(repeats)) + "."
        # print(groups[:-1])
        groups = ",".join(groups[:-1] for i in range(repeats))
        # print(row, groups)
        rows.append((row, list(map(int, groups.split(",")))))
    return rows


def pattern_from_groups(group):
    return r"^([.?]*?)" + r"[#?]{" + str(group) + "}" + r"[^#]"


@cache
def count_arrangements(row, groups, start_row, start_groups):
    if start_groups >= len(groups):
        if "#" in row[start_row:]:
            return 0
        else:
            return 1
    m = re.match(pattern_from_groups(groups[start_groups]), row[start_row:])
    if m:
        start_row += len(m.group(1))
        dig = count_arrangements(
            row, groups, start_row + groups[start_groups] + 1, start_groups + 1
        )
        if row[start_row].startswith("?"):
            scan = count_arrangements(row, groups, start_row + 1, start_groups)
        else:
            scan = 0
        return dig + scan
    else:
        return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    rows = parse_input(L)
    possibilities = 0
    for i, (row, groups) in enumerate(rows):
        for j in range(4, 0, -1):  # precompute segments from later
            count_arrangements(
                row, tuple(groups), len(row) * j // 5, len(groups) * j // 5
            )
        p = count_arrangements(row, tuple(groups), 0, 0)
        print("***", i, "***", row, groups, p)
        possibilities += p
    print(possibilities)
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

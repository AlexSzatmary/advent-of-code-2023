#!/usr/bin/env python
# from itertools import cycle
import re
import sys


def parse_input(L):
    rows = []
    for s in L:
        row, groups = s.split(" ")
        repeats = 5
        row = "?".join(row for i in range(repeats))
        # print(groups[:-1])
        groups = ",".join(groups[:-1] for i in range(repeats))
        # print(row, groups)
        rows.append((row, list(map(int, groups.split(",")))))
    return rows


def pattern_from_groups(groups):
    return (
        r"^([.?]*?)"
        + r"[.?]+".join(r"[#?]{" + str(i) + "}" for i in groups)
        + r"[^#]*$"
    )


def count_arrangements(row, groups, memo):
    # breakpoint()
    if not groups:
        return 1
    if (row, tuple(groups)) in memo:
        return memo[row, tuple(groups)]
    m = re.match(pattern_from_groups(groups), row)
    if m:
        start = len(m.group(1))
        dig = count_arrangements(row[start + groups[0] + 1 :], groups[1:], memo)
        if row[start].startswith("?"):
            scan = count_arrangements(row[start + 1 :], groups, memo)
        else:
            scan = 0
        memo[(row, tuple(groups))] = dig + scan
        return memo[(row, tuple(groups))]
    else:
        memo[(row, tuple(groups))] = 0
        return memo[(row, tuple(groups))]


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    rows = parse_input(L)
    possibilities = 0
    for row, groups in rows:
        p = count_arrangements(row, groups, {})
        print(row, groups, p)
        possibilities += p
    print(possibilities)


if __name__ == "__main__":
    sys.exit(main())

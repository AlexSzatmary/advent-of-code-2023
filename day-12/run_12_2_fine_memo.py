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


def count_arrangements(row, groups, start_row, start_groups, memo):
    if (start_row, start_groups) in memo:
        return memo[(start_row, start_groups)]
    # breakpoint()
    my_row = row[start_row:]
    my_groups = groups[start_groups:]
    if not my_groups:
        return 1
    m = re.match(pattern_from_groups(my_groups), my_row)
    if m:
        start_row += len(m.group(1))
        dig = count_arrangements(
            row, groups, start_row + my_groups[0] + 1, start_groups + 1, memo
        )
        if row[start_row].startswith("?"):
            scan = count_arrangements(row, groups, start_row + 1, start_groups, memo)
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
    rows = parse_input(L)
    possibilities = 0
    for i, (row, groups) in enumerate(rows):
        p = count_arrangements(row, groups, 0, 0, {})
        print("***", i, "***", row, groups, p)
        possibilities += p
    print(possibilities)


if __name__ == "__main__":
    sys.exit(main())

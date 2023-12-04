#!/usr/bin/env python
import numpy as np
import re
import sys


def syms_from_L(L):
    return np.array(
        [[1 if (not c.isnumeric() and c != ".") else 0 for c in s[:-1]] for s in L]
    )


def add_matching_parts(L):
    syms = syms_from_L(L)
    count = 0
    for i, s in enumerate(L):
        for m in re.finditer(r"\d+", s):
            if np.any(
                syms[
                    max(0, i - 1) : min(i + 1 + 1, np.size(syms, 0)),
                    max(0, m.start() - 1) : min(m.end() + 1, np.size(syms, 1)),
                ]
            ):
                count += int(m.group())
    return count


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
        print(add_matching_parts(L))


if __name__ == "__main__":
    sys.exit(main())

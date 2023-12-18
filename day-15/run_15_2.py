#!/usr/bin/env python
from collections import OrderedDict
import re
import sys
import timeit


def parse_input(L):
    return L[0].split(",")


def h(s):
    a = 0
    for c in s:
        a = (a + ord(c)) * 17 % 256
    return a


def arrange_boxes(steps):
    boxes = [OrderedDict() for _ in range(256)]
    for step in steps:
        m = re.match("(.*)([-=])(.*)", step)
        label = m.group(1)
        op = m.group(2)
        if op == "=":
            boxes[h(label)][label] = int(m.group(3))
        else:
            if label in boxes[h(label)]:
                boxes[h(label)].pop(label)
    return boxes


def find_focusing_power(boxes):
    fp = 0
    for i, box in enumerate(boxes):
        for j, (lens_label, focal_length) in enumerate(box.items()):
            fp += (i + 1) * (j + 1) * focal_length
    return fp


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    steps = parse_input(L)
    boxes = arrange_boxes(steps)
    print(find_focusing_power(boxes))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

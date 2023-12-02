#!/usr/bin/env python
import re
import sys

# L = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
# Lb = ["two1nine", "eightwothree", "abcone2threexyz", "xtwone3four",
# "4nineeightseven2", "zoneight234", "7pqrstsixteen"]

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def add_calibration_values(L):
    c = 0
    for s in L:
        s1 = re.match(r"^\D*(.+?)\D*$", s).group(1)
        c += int(s1[0] + s1[-1])
    return c


def add_calibration_valuesb(L):
    c = 0
    for s in L:
        digit_1 = re.search(r"(" + "|".join(DIGITS.keys()) + r"|\d)", s).group(1)
        if digit_1 in DIGITS:
            digit_1 = DIGITS[digit_1]
        digit_2 = re.search(r".*(" + "|".join(DIGITS.keys()) + r"|\d)", s).group(1)
        if digit_2 in DIGITS:
            digit_2 = DIGITS[digit_2]
        c += int(digit_1 + digit_2)
    return c


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1]) as hin:
        L = hin.readlines()
    print(add_calibration_valuesb(L))


if __name__ == "__main__":
    sys.exit(main())

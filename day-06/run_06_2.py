#!/usr/bin/env python
import math
import re
import sys

# math scratch work
# my distance
# my_distance = my_button_time * (time - my_button_time)
# my_button_time * (time - my_button_time) > record_distance
# my_button_time * time - my_button_time ** 2 - record_distance > 0
# my_button_time ** 2 - my_button_time * time + record_distance < 0
# my_button_time < (time +/- sqrt(time ** 2 - 4 * record_distance)) / 2
# possibilities = sqrt(time ** 2 - 4 * record_distance)


def parse_input(L):
    times = int("".join(re.findall(r"\d+", L[0])))
    distances = int("".join(re.findall(r"\d+", L[1])))
    return times, distances


def brute_force(time, distance):
    c = 0
    for i in range(time):
        if i * (time - i) > distance:
            c += 1
    return c


def magic(time, distance):
    return round(math.sqrt(time**2 - 4 * distance - 4) / 2) * 2 - (time + 1) % 2


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    time, distance = parse_input(L)
    # print(
    #     math.prod(
    #         [magic(time, distance) for time, distance in zip(times, distances)]
    #     )
    # )
    print(magic(time, distance))


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
from collections import Counter
import sys

CARD_TO_INT = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def parse_hand(hand_str):
    return [CARD_TO_INT[c] for c in hand_str]


def parse_input(L):
    hands = []
    bids = []
    for s in L:
        hand_str, bid_str = s.split()
        hands.append(parse_hand(hand_str))
        bids.append(int(bid_str))
    return hands, bids


def score_hand(hand):
    if 1 in hand:  # deal with jokers
        c = Counter(hand)
        mc = sorted(c.most_common(), key=lambda x: (x[1], x[0]), reverse=True)
        # sort card groups by count then value
        for (card, count) in mc:  # find the biggest group that isn't 1's
            if card == 1:
                if count == 5:
                    best = 1
                    break
            else:
                best = card
                break
        hand = [card if card != 1 else best for card in hand]  # replace jokers
    c = Counter(hand)
    mc = c.most_common()
    if mc[0][1] == 5:
        return 5.
    elif mc[0][1] == 4:
        return 4
    elif mc[0][1] == 3 and mc[1][1] == 2:  # full house
        return 3.5
    elif mc[0][1] == 3:
        return 3
    elif mc[0][1] == 2 and mc[1][1] == 2:  # two pair
        return 2.5
    elif mc[0][1] == 2:
        return 2
    else:
        return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    hands, bids = parse_input(L)
    scores = list(map(score_hand, hands))
    scored_tup = sorted(zip(scores, hands, bids))
    winnings = 0
    for i, (score, hand, bid) in enumerate(scored_tup):
        winnings += (i + 1) * bid
    print(winnings)


if __name__ == "__main__":
    sys.exit(main())

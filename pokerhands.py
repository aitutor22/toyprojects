#Euler problem 54
import collections

def numeric_value(num):
    values = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }
    return values[num] if num in values else int(num)

#sort according to descending numeric value
#useful for determining tiebreak for flushes and straights
def sort_by_numeric_value(hand, return_only_number=None):
    result = sorted(hand, key=lambda x: numeric_value(x[0]), reverse=True)

    if return_only_number:
        return [numeric_value(n[0]) for n in result]
    else:
        return result

#sort and places pairs/3 of a kind/four of a kind in front
#note that this returns a list of the numeric part of a card (i.e. T, J, 8)
def sort_according_to_pairs(hand):
    nums = [c[0] for c in hand]
    counter = collections.Counter(nums)
    temp = [c for c in counter.most_common(5)]

    temp = sorted(temp, key=lambda x: numeric_value(x[0]), reverse=True)
    temp = sorted(temp, key=lambda x: x[1], reverse=True)

    result = []
    #n stands for the number, f stands for the number of times it appears
    for n, f in temp:
        result += [numeric_value(n)] * int(f)
    return result

#returns True if it is a straight, where n is the number of the largest card; else False
def isstraight(hand):
    hand = sort_by_numeric_value(hand)
    nums = [numeric_value(c[0]) for c in hand]

    #hand is a straight if each card is one less than the preceding card
    for index, n in enumerate(nums):
        if index == 0:
            continue

        if n != nums[index - 1] - 1:
            return False
    return True

#returns True if all cards in hand contains the same suit
def isflush(hand):
    #tests if all the cards have the same suit as the first card
    return all([c[-1] == hand[0][-1] for c in hand])

#returns a list containing duplicates (only the number is returned)
def getduplicates(hand):
    nums = [c[0] for c in hand]
    counter = collections.Counter(nums)
    return [c[1] for c in counter.most_common(5) if c[1] > 1]

def ispair(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 2

def istwopair(duplicates):
    return len(duplicates) == 2 and duplicates[0] == 2 and duplicates[1] == 2

def isthreofakind(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 3

def isfullhouse(duplicates):
    return len(duplicates) == 2 and duplicates[0] == 3 and duplicates[1] == 2

def isfourofakind(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 4

def getranking(hand):
    hand = sort_by_numeric_value(hand)
    straight = isstraight(hand)
    flush = isflush(hand)

    duplicates = getduplicates(hand)
    fourofakind = isfourofakind(duplicates)
    fullhouse = isfullhouse(duplicates)
    threeofakind = isthreofakind(duplicates)
    twopair = istwopair(duplicates)
    pair = ispair(duplicates)

    if straight and flush:
        return 10 if hand[0][0] == "A" else 9
    elif fourofakind:
        return 8
    elif fullhouse:
        return 7
    elif flush:
        return 6
    elif straight:
        return 5
    elif threeofakind:
        return 4
    elif twopair:
        return 3
    elif pair:
        return 2
    else:
        return 1

#to break ties, we compare highest card for both hands and move to next card in event of a tie
#for hands with flushes, straights and high card, we should sort according to numeric_value
#for pairs, etc, we should place the pairs in front
def break_tie(hand1, hand2):
    ranking = getranking(hand1)

    if ranking in [10, 9, 6, 5, 1]:
        hand1 = sort_by_numeric_value(hand1, True)
        hand2 = sort_by_numeric_value(hand2, True)
    else:
        hand1 = sort_according_to_pairs(hand1)
        hand2 = sort_according_to_pairs(hand2)

    for index, _ in enumerate(hand1):
        if hand1[index] == hand2[index]:
            continue
        else:
            return hand1[index] > hand2[index]

def compare(row):
    cards = row.split(" ")
    p1 = cards[0:5]
    p2 = cards[5:]
    
    p1_ranking = getranking(p1)
    p2_ranking = getranking(p2)

    return break_tie(p1, p2) if p1_ranking == p2_ranking else p1_ranking > p2_ranking

if __name__ == "__main__":
    with open("poker.txt") as f:
        wins = 0

        rows = [row for row in f.read().split("\n") if len(row) > 0]
        for row in rows:
            if compare(row):
                wins += 1

        print(wins)
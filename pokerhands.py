#Euler problem 54
import timeit
import collections

def get_numeric_value(num):
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
def sort_by_get_numeric_value(hand, return_only_number=None):
    result = sorted(hand, key=lambda x: get_numeric_value(x[0]), reverse=True)

    if return_only_number:
        return [get_numeric_value(n[0]) for n in result]
    else:
        return result

#sort and places pairs/3 of a kind/four of a kind in front
#note that this returns a list of the numeric part of a card (i.e. T, J, 8)
def sort_according_to_pairs(hand):
    nums = [get_numeric_value(c[0]) for c in hand]
    common = [c for c in collections.Counter(nums).most_common(5)]

    common.sort(key=lambda x: x[1] * 100 + x[0], reverse=True)

    result = []
    #n stands for the number, f stands for the number of times it appears
    for n, f in common:
        result += [n] * int(f)
    return result

#returns (True, n) if it is a straight, where n is the number of the largest card; else (False, None)
def is_straight(hand):
    nums = sort_by_get_numeric_value(hand, True)

    #hand is a straight if current card is one greater than the next card
    for curr_card, next_card in zip(nums[:-1], nums[1:]):
        if curr_card != next_card + 1:
            return (False, None)

    return (True, nums[0])

#returns True if all cards in hand contains the same suit
def is_flush(hand):
    #tests if all the cards have the same suit as the first card
    return all([c[-1] == hand[0][-1] for c in hand])

#returns a list containing duplicates (only the number is returned)
def get_duplicates(hand):
    nums = [c[0] for c in hand]
    counter = collections.Counter(nums)
    return [c[1] for c in counter.most_common(5) if c[1] > 1]

def is_pair(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 2

def is_two_pair(duplicates):
    return len(duplicates) == 2 and duplicates[0] == 2 and duplicates[1] == 2

def is_three_of_a_kind(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 3

def is_full_house(duplicates):
    return len(duplicates) == 2 and duplicates[0] == 3 and duplicates[1] == 2

def is_four_of_a_kind(duplicates):
    return len(duplicates) == 1 and duplicates[0] == 4

def get_ranking(hand):
    straight, highest_card = is_straight(hand)
    flush = is_flush(hand)

    duplicates = get_duplicates(hand)

    if straight and flush:
        return 10 if highest_card == "A" else 9
    elif is_four_of_a_kind(duplicates):
        return 8
    elif is_full_house(duplicates):
        return 7
    elif flush:
        return 6
    elif straight:
        return 5
    elif is_three_of_a_kind(duplicates):
        return 4
    elif is_two_pair(duplicates):
        return 3
    elif is_pair(duplicates):
        return 2
    else:
        return 1

#to break ties, we compare highest card for both hands and move to next card in event of a tie
#for hands with flushes, straights and high card, we should sort according to get_numeric_value
#for pairs, etc, we should place the pairs in front
def break_tie(hand1, hand2):
    ranking = get_ranking(hand1)

    if ranking in [10, 9, 6, 5, 1]:
        hand1 = sort_by_get_numeric_value(hand1, True)
        hand2 = sort_by_get_numeric_value(hand2, True)
    else:
        hand1 = sort_according_to_pairs(hand1)
        hand2 = sort_according_to_pairs(hand2)

    for card1, card2 in zip(hand1, hand2):
        if card1 == card2:
            continue
        else:
            return card1 > card2

def compare(row):
    cards = row.split(" ")
    p1 = cards[0:5]
    p2 = cards[5:]
    
    p1_ranking = get_ranking(p1)
    p2_ranking = get_ranking(p2)

    return break_tie(p1, p2) if p1_ranking == p2_ranking else p1_ranking > p2_ranking

def run():
    with open("poker.txt") as f:
        wins = 0

        rows = [row for row in f.read().split("\n") if len(row) > 0]
        for row in rows:
            if compare(row):
                wins += 1

        # print(wins)    

if __name__ == "__main__":
    print(timeit.timeit(run, number=100))

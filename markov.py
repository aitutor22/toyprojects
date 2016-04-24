import collections
import random

f_input = open("speeches.txt", "r", encoding="utf-8")
text = f_input.read().replace("\n", " ")

text = "".join([c for c in text if c not in ",.?:;'\"!“”‘’-/\\(),"])
data = [w for w in text.lower().split(" ") if w != ""]

def create_transition_table(data):
    counts = collections.defaultdict(dict)
    transitions = collections.defaultdict(dict)

    #creates a count table
    for pos, word in enumerate(data[:-1]):
        next_word = data[pos + 1]
        counts[word][next_word] = counts[word].setdefault(next_word, 0) + 1

    #creates a transition table
    for k, v in counts.items():
        total = sum(v.values())
        for k2, v2 in v.items():
            transitions[k][k2] = v2 / total

    return transitions

#takes a transition table and a word, returns the next word
def next_word(table, word):
    probability = random.random()
    cum_probability = 0

    for k, v in table[word].items():
        cum_probability += v

        if probability <= cum_probability:
            selected_word = k
            break

    return selected_word

table = create_transition_table(data)

w = "good"
generated_words = [w]
for _ in range(20):
    w = next_word(table, w)
    generated_words.append(w)

print(" ".join(generated_words))

import string
import collections

#START INPUT VARIABLES
#use encoding of utf-8 to prevent issues with special characters
f_input = open("speeches.txt", "r", encoding="utf-8")
f_output = open("output.txt", "w", encoding="utf-8")

#words that we do not wish to include in the count
exclude = ["the", "and", "in", "a", "of", "to", "is", "are", 
           "have", "this", "that", "for", "it", "or", "they"]

#show how many top entries
top_entries = 50
#END INPUT VARIABLES

#assumption is it's okay to use lower version of text since we are just counting
text = f_input.read().lower()

#removes punctuations
text = "".join([c for c in text if c not in ",.?:;'\"!“”‘’-/\\(),"])
#removes new lines
text = text.replace("\n", " ")

words = text.split(" ")
#removes words from exclude list
words = [word for word in words if word not in exclude]

#calculates most common words
counter = collections.Counter(words)
results = counter.most_common(top_entries)

for keyword, count in results:
    f_output.write("{}, {}\n".format(keyword, count))

f_output.close()
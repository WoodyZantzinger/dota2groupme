import re
from collections import Counter
import string

with open("utils/emulate/stop_words.txt") as inputfile:
        blacklist = inputfile.read().splitlines()

word_counter = Counter()

with open("utils/emulate/rawtext_history.txt", "rU", encoding="utf-8") as f:
    for line in f:
        word_counter.update(line.lower().split())

def key_words(msg):

    results = {}
    total_weight = 0

    for word in msg.lower().split():
        if word not in blacklist:
            results[word] = word_counter[word]
            total_weight = total_weight + word_counter[word]

    return results

def word_occurance(word):
    return word_counter[word]
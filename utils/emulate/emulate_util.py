import re
import os
from collections import Counter
import string

with open(os.path.join(os.path.dirname(__file__), 'stop_words.txt')) as inputfile:
        blacklist = inputfile.read().splitlines()

word_counter = Counter()

with open(os.path.join(os.path.dirname(__file__), 'rawtext_history.txt'), "rU") as f:
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
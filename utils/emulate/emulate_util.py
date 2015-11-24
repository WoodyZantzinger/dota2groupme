import re

with open("utils/emulate/stop_words.txt") as inputfile:
        blacklist = inputfile.read().splitlines()

file = open("utils/emulate/rawtext_history.txt","r")
inputString = file.read()
word_list = re.split('\s+', inputString.lower())

def key_words(msg):

    results = {}
    total_weight = 0

    for word in msg.lower().split():
        if word not in blacklist:
            results[word] = word_list.count(word)
            total_weight = total_weight + word_list.count(word)

    return results
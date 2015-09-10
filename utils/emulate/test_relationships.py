import sys
import json
import re

__author__ = 'woodyzantzinger'

blacklist = []

def key_words(msg):

    results = {}
    total_weight = 0

    for word in msg.lower().split():
        if word not in blacklist:
            results[word] = word_list.count(word)
            total_weight = total_weight + word_list.count(word)

    return results

if(len(sys.argv) < 2):
    print "Enter a data file to parse"
else:
    with open(sys.argv[1]) as data_file:
        relationship_data = json.load(data_file)

    with open("stop_words.txt") as inputfile:
        blacklist = inputfile.read().splitlines()

    file = open("rawtext_history.txt","r")
    inputString = file.read()
    word_list = re.split('\s+', inputString.lower())

    while 1:
        input = raw_input("Enter the word to see relationships: ")

        keys = key_words(input)

        result_set = []

        for key in keys:
            if key in relationship_data:
                if len(result_set) == 0:
                    result_set = relationship_data[key]
                    print "Empty Set so lets input for " + key
                    print result_set
                else:
                    result_set = [k for k in relationship_data[key] if k in result_set]
                    print "Collision leads to testing against " + key
                    print relationship_data[key]
                    print result_set

        print result_set
import sys
import json
import re
import pdb
from senGen import *

from operator import itemgetter

__author__ = 'woodyzantzinger'

blacklist = []
word_list = []

def key_words(msg):

    results = {}
    total_weight = 0

    for word in msg.lower().split():
        if word not in blacklist:
            results[word] = word_list.count(word)
            total_weight = total_weight + word_list.count(word)

    return results

def generate_response(input, debug = 0):

    output = ""

    with open("utils/emulate/relationships.json") as data_file:
        relationship_data = json.load(data_file)

    with open("utils/emulate/stop_words.txt") as inputfile:
        blacklist = inputfile.read().splitlines()

    file = open("utils/emulate/rawtext_history.txt","r")
    inputString = file.read()
    word_list = re.split('\s+', inputString.lower())

    keys = key_words(input)

    if debug:
        output += "I think your question is about: "
        for key in keys:
            output += key + ", "
        output += "\n"

    result_set = []

    for key in keys:
        if key in relationship_data:

            if len(result_set) == 0:
                result_set = relationship_data[key]
            else:
                for newKey in relationship_data[key]:
                    if newKey in result_set:
                        result_set[newKey] += 1
                    else:
                        result_set[newKey] = 1
                # result_set = [k for k in relationship_data[key] if k in result_set]

    #for key in sorted(result_set, key=itemgetter(1), reverse=True):

    word_list = []

    sum = 0.0
    if len(result_set) > 0:
        for key in sorted(result_set, key=result_set.get):
            result_set[key] = result_set[key] ** 3
            sum += result_set[key]

            #print key, result_set[key]

        if debug:
            output += "I think I should respond with: "
        for key in sorted(result_set, key=result_set.get):
            weight = result_set[key] / sum
            if weight > .03:
                if debug: output += key + ": " + str(weight * 100) + "%, "
                word_list.append(key)
        if len(word_list) < 1:
            # we couldn't find a meaningful pattern!
            # print result_set
            output += "I don't have confidence in any response"
        else:

            for key in keys:
                word_list.append(key)
            output += "\n" + make_sentence(word_list)
    else:
        output += "I don't understand what your message means"
    return output

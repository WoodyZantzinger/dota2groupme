import sys
import json
import re
import pdb
from senGen import *
from collections import defaultdict
import emulate_util
import operator

from operator import itemgetter

__author__ = 'woodyzantzinger'

MIN_CUTOFF = .95

#@profile
def generate_response(input, debug = 0):

    output = ""

    with open("utils/emulate/relationships.json") as data_file:
        relationship_data = json.load(data_file)

    key_words = emulate_util.key_words(input)
    total_sentence_weight = sum(key_words.values()) * 1.0

    print input

    #convert to % then inverse (The result is a %)
    for key_word in key_words:
        key_words[key_word] = (1.0 - (key_words[key_word] / total_sentence_weight))
        print key_word + ": " + str(key_words[key_word] * 1) + ""

    #these are the "result words" which come from our key words in the sentence
    #The algorithm = key_word(% score) * (result_word(score) / occurance of results word)


    result_set = defaultdict(int)

    for key_word in key_words:
        if key_word in relationship_data:
            for result_word in relationship_data[key_word]:
                occurance = emulate_util.word_occurance(result_word) * 2
                word_score = 0
                if occurance > 0: word_score = key_words[key_word] * ( relationship_data[key_word][result_word] / occurance )
                if word_score > .4: result_set[result_word] += word_score

   # for result_word in sorted(result_set, key=result_set.get):
        #print result_word + " : " + str(result_set[result_word])

    #Trim anything that doesn't make the cut of AT LEAST the MIN_CUTOFF value

    #final_words = {k: v for k, v in result_set.items() if k > MIN_CUTOFF}
    final_words = dict(sorted(result_set.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])

    print final_words

    return make_sentence(final_words.keys())

print generate_response("Andy licks butt")
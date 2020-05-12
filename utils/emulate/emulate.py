import sys
import json
import re
import pdb
from .senGen import *
from collections import defaultdict
from utils.emulate import emulate_util
import operator
import nltk

from operator import itemgetter

__author__ = 'woodyzantzinger'

#@profile
def generate_response(input, debug = 0):

    output = ""

    with open("utils/emulate/relationships.json") as data_file:
        relationship_data = json.load(data_file)

    key_words_temp = emulate_util.key_words(input)
    key_words = {}
    total_sentence_weight = sum(key_words_temp.values()) * 1.0

    if len(key_words_temp) < 1: return "I didn't understand your dumbass message"

    if debug: output += "Input Keywords: "

    #convert key_word to add Type of Speech
    key_word_pos = nltk.pos_tag(nltk.word_tokenize(input))
    for word in key_words_temp:
        for word_with_pos in key_word_pos:
            if word == word_with_pos[0].lower():
                key_words[word + "#" + word_with_pos[1]] = key_words_temp[word]

    #if Multiple words, convert to % then inverse (The result is a %)
    if len(key_words) > 1:
        for key_word in key_words:
            key_words[key_word] = (1.0 - (key_words[key_word] / total_sentence_weight))
            if debug: output += key_word + ": " + str(key_words[key_word] * 1) + "\n"



    #these are the "result words" which come from our key words in the sentence
    #The algorithm = key_word(% score) * (result_word(score) / occurance of results word)
    result_set = defaultdict(int)
    #pdb.set_trace()
    for key_word in key_words:
        if key_word in relationship_data:
            for result_word in relationship_data[key_word]:
                occurance = emulate_util.word_occurance(result_word.split("#", 1)[0]) * 2
                word_score = 0
                if occurance > 0:
                    word_score = key_words[key_word] * ( relationship_data[key_word][result_word] / occurance )
                    result_set[result_word] += word_score

   # for result_word in sorted(result_set, key=result_set.get):
        #print result_word + " : " + str(result_set[result_word])

    #Trim anything that doesn't make the cut of AT LEAST the MIN_CUTOFF value

    #final_words = {k: v for k, v in result_set.items() if k > MIN_CUTOFF}
    sorted_words = dict(sorted(result_set.items(), key=operator.itemgetter(1), reverse=True)[:5])
    final_words = []

    for word in sorted_words:
        final_words.append(word.split("#", 1)[0])

    #pdb.set_trace()

    if debug: output += "Response Keywords: " + str(final_words) + "\n\n"

    if len(final_words) < 1:
        output += "I don't understand..."
    else:
        output += make_sentence(final_words)

    return output
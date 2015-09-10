import re
import nltk
import sys
import json
import pdb
from progressbar import ProgressBar

def key_words(msg):

    results = {}
    total_weight = 0

    for word in msg.lower().split():
        if word not in blacklist:
            results[word] = word_list.count(word)
            total_weight = total_weight + word_list.count(word)

    return results


if(len(sys.argv) < 4):
    print "Enter a data file to parse, a blacklist of common words, and a message history (JSON file)"
else:
    file = open(sys.argv[1],"r")
    inputString = file.read()
    word_list = re.split('\s+', inputString.lower())

    blacklist = []
    message_data = []

    with open(sys.argv[3]) as data_file:
        message_data = json.load(data_file)

    with open(sys.argv[2]) as inputfile:
        blacklist = inputfile.read().splitlines()

    relationships = {}

    print "TOTAL MESSAGES"
    print len(message_data[:len(message_data)/10])

    pbar = ProgressBar(
        maxval=len(message_data[:len(message_data)/10]),
    )


    for index, message in pbar(enumerate(message_data[:len(message_data)/10])):
        text = message["text"]
        time = message["created_at"]
        if index == (len(message_data) - 1):
            break #we hit the last message!
        previous_message = message_data[index + 1]
        response_time = time - previous_message["created_at"]
        if response_time > 1000 or previous_message["text"] == None or text == None:
            continue #the next message might not have been tied to this one or one of the messages was blank

        message_weight = key_words(text)
        previous_message_weight = key_words(previous_message["text"])

        for result_key in message_weight:
            for next_key in previous_message_weight:
                #print next_key + " leads to " + result_key
                #pdb.set_trace()
                if next_key not in relationships:
                    relationships[next_key] = {}
                if result_key not in relationships[next_key]:
                    relationships[next_key][result_key] = 0
                relationships[next_key][result_key] += previous_message_weight[next_key]

    with open("relationships.json", 'w') as outfile:
        json.dump(relationships, outfile)

    print "Number of Unique Relationships:"
    print len(relationships)

import json
import emulate_util

def response(msg):

    with open("relationships.json") as data_file:
        relationships = json.load(data_file)

    key_words = emulate_util.key_words(msg)

    final_response = ""
    final_highest_value = 0.0

    for word in key_words:
        if word in relationships:
            best_response = ""
            highest_value = 0.0
            sum = 0.0
            for response in relationships[word]:
                if relationships[word][response] > highest_value:
                    highest_value = relationships[word][response]
                    best_response = response
                sum += relationships[word][response]
            highest_value = highest_value / sum
            if highest_value > final_highest_value:
                final_highest_value = highest_value
                final_response = best_response

    return final_response
Starting a Emulation README

# Files

#### Python Files
* **Emulate.py:** This is where an input sentence is turned into a reponse. The function `def generate_response(input, debug = 0)` is the starting point for understanding how the system works.
* **find_important.py:** This file is only run once to generate the relationships JSON file. It parses through the  GroupMe Chat history and outputs a relationship file.
* **get_messages.py:** This file is only run once to download the GroupMe text history. It currently needs to be manually edited to either output the JSON GroupMe Responses (needed for find_important.py) or the raw text messages (needed for senGen.py). This file was used to create both "message_history.json" and "rawtext_history.txt".
* **senGen.py**: This file generates sentences with a set "Markov Length" and a list of target "White Words". I took this from somewhere online an edited it. The function `def make_sentence(white_list):` beings the process. Right now the Markov Length is at a fixed "2".

#### Important Input Files
* **rawtext_history.txt**: This is a raw text output of the entire Group's message history. This is used to generate realistic sounding sentences
* **stop_words.txt**: This is a list of [Stop Words](https://en.wikipedia.org/wiki/Stop_words) which are filtered out when processing sentences for relationships
* **relationships.JSON**: This is the saved JSON for the relationships between words. The current version is run from all ~20,000 messages.

#### Deprecated:
* **test_relationships**: This was an old file used to test the output of the "find_important" process.
* **jon.txt* and *mike.txt**: The raw message history of just Jon and Mike. These can be input to make sUN use only Jon and Mike sentences

# Theory

To explain how the system works below is an example from our chat history to reference:
```
D: Wait you son of a bitch this is a large sausage piza hahahha
A: Rekt
J: Awww
J: LOL
J: Did you also get the coke
D: Yeah also he gave me a drink
J: Good.
D: You're good.
```

#### Prep Work

**find_important.py** goes through our history to look for messages and their response. Right now basically every message is considered a response to the previous message.

Stop_words are stripped from both the original and response message. In the above this would lead to the above set:
```
  message_key_words = ["Wait", "son", "bitch", "sausage", "pizza", "hahahha"]
  result_key_words = ["Rekt"]
```

It then updates a dictionary of relationships. So after parsing the above the system assumes all the `message_key_words` lead to the `result_key_words`. If a future message containing the keyword "Pizza" is encountered again, its adds the new keywords to the same dictionary. If a word is encountered which is already in the dictionary, its occurance is incremented so it looks like the below:

```
"woods": {
  "poop": 1, 
  "good": 1, 
  "candidate.": 1, 
  "treant": 1, 
  "son": 1, 
  "note": 1, 
  "earlier?": 1, 
  "slowly": 1, 
  "bitch": 1, 
  "talks": 1, 
  "woody": 1, 
  "bit": 1, 
  "protector": 1, 
  "hate": 1, 
  "smells": 2}
```

This means every occurance of woods is likely to have the following words in its response. "smells" came up twice in responses.

This is stored in **relationships.JSON**

#### Generating Responses

For this example lets assume the input to #oracle is `#oracle woods` and we can use the relationships example above.

**emulate.py** creates a response by stripping the input of Stop Words and looking for the relationships asociated with the input key words. It then attempts to pick out the obvious outliers to find which response is most likely.

If no outliers are found, it doesn't know what to respond with so it returns `I don't have confidence in any response`

If an outlier is found (for example "smells" above which occured twice in responses to "woods" as opposed to once for every other word) it moves on to generating a sentence with the topic words. This is done through **senGen.py** which takes the list of keywords as input.

**senGen.py** simply generates a Markov Chain which is used to make somewhat sensical sentences from a set of conversation. The Length of the chain can be increased to make the sentences seem more realistic at the expense of randomness. From experimenting chain length of 4 and beyond will simply return actual historical responses (e.g. Thing we literally said in chat history).

So the sentence stays on topic, *senGen.py* will only use chat history which references the supplied "white list" of words. In this example that would be any message which contains "smells".

This doesn't mean the response will neccesarily contain the word "smells" only that the sample set will be made up of the words in messages which reference "smells".


#### Future Improvements

* sUN messages need to be taken out of the prep work. They throw off the relationship between messages by adding a lot of noise into the system
* senGen could do a better job of generating sentences actually about the supplied topic. If 3+ general topics are supplied (.i.e "Andy", "Woody", "Mike") so many messages meet the criteria it essentially is just a random sample.
* Better rules for determining if a message is the result of the message before it. Right now almost every message is included even if it is a long delay or someone replying to themselves (which could be OK?)

import requests, json

with open("li-urban.json", "r") as definition_file:
    definitions = json.loads(definition_file.read())

all_words = ""
for n, definition in enumerate(definitions["list"]):
    # print(n," ", definition["definition"], "\n")
    all_words += definition["definition"] + " "
# print(all_words)
list_of_common_words = ["is", "a", "the", "to", "and", "you", "of", "not", "for"
                        "it", "when", "it", "out", "as", "in", "are", "they"]
most_words = ""
for word in all_words.split():
    if word.lower() not in list_of_common_words and word.isalpha():
        most_words += word + " "
# print(definitions)
frequency = {}
for word in most_words.split():
    frequency[word] = frequency.get(word, 0) + 1

for word in sorted(frequency, key=frequency.get, reverse=True):
  print(word, frequency[word])# print(most_words)
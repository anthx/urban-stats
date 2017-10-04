import requests, json

with open("cat-urban.json", "r") as definition_file:
    definitions = json.loads(definition_file.read())

all_words = ""
for n, definition in enumerate(definitions["list"]):
    # print(n," ", definition["definition"], "\n")
    all_words += definition["definition"] + " "
# print(all_words)
list_of_common_words = ["that", "with", "the", "to", "and", "you", "of", "not", "for",
                        "have", "when", "out", "as", "in", "are", "they", "your", "who", "all"]
most_words = []
for word in all_words.split(" "):
    # if "." in word: print(word.isalpha())
    if (word.lower() not in list_of_common_words and
            not word.isnumeric() and len(word) > 3 and "\n" not in word):
        most_words.append(word)
# print(definitions)
frequency = {}
for word in most_words:
    frequency[word] = frequency.get(word, 0) + 1

print("number of words: ", len(most_words))

for word in sorted(frequency, key=frequency.get, reverse=True):
    percent = frequency[word]/len(most_words)*100
    print(word, frequency[word], str(round(percent, 2))+"%")
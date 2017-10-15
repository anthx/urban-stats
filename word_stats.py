import requests, json, re

with open("cat-urban.json", "r") as definition_file:
    definitions = json.loads(definition_file.read())

all_words = ""
for n, definition in enumerate(definitions["list"]):
    # print(n," ", definition["definition"], "\n")
    all_words += definition["definition"] + " "

list_of_common_words = ["that", "with", "the", "to", "and", "you", "of", "not", "for", "them",
                        "have", "when", "out", "as", "in", "are", "they","their", "your", "who", "all"]
most_words = []
for word in re.split("[,. ]", all_words):
    # if "." in word: print(word.isalpha())
    if (word.lower() not in list_of_common_words and
            not word.isnumeric() and len(word) > 3 and "\n" not in word):
        # for letter in word:
        #     if word[0] in [".", ]
        most_words.append(word)
# print(definitions)


print("number of (useful) words: ", len(most_words))

print("\nTop 10 Words by frequency")
frequency = {}
for word in most_words:
    frequency[word] = frequency.get(word, 0) + 1

top_words = []
for i, word in enumerate(sorted(frequency, key=frequency.get, reverse=True)):
    if i < 10:
        top_words.append(word)
        percent = frequency[word]/len(most_words)*100
        print(word, frequency[word], str(round(percent, 2))+"%")
    else:
        break

print("\nEnding in Y\n")
for word in most_words:
    if word[-1] == "y":
        print(word)

print("\nEnding in D\n")
for word in most_words:
    if word[-1] == "d":
        print(word)

print("\nShort Words\n")
for word in most_words:
    if len(word) < 5 :
        print(word)

print("\nLong Words\n")
for word in most_words:
    if len(word) >= 5:
        print(word)

print("\nSentences containing the top words\n")
sentences = []
for word in re.split("[!?.\t]|[\r\n]|[\n]", all_words):
    # if "." in word: print(word.isalpha())
    # if (word.lower() not in list_of_common_words and
    #         not word.isnumeric() and len(word) > 3):
    # print(word.strip(), "\n")
    sentences.append(word.strip())

for sentence in sentences:
    for top in top_words:
        if top in sentence:
            print(sentence)
            break


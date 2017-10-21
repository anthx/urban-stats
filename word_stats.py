import requests, json, re, sys
from jinja2 import exceptions, Environment, BaseLoader, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def words_ending_in(word_list: list, string: str) -> list:
    """
    Returns a new list of words from word_list where ending letters match string
    :param word_list: a list of words
    :param string: the string to match
    :return: a new list of words
    """
    result = []
    for each in word_list:
        if each[0-len(string):] == string:
            result.append(each)
    return result


most_words = ["five", "dog", "sexy"]
all_words = "The cat sat on the mat"
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
for word in words_ending_in(most_words, "y"):
    print(word)

print("\nEnding in D\n")
for word in words_ending_in(most_words, "d"):
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


def eng_sentence_splitter(text):
    sentences = []
    for i, fragment in enumerate(re.split("([!?.\t]|[\r\n]|[\n])", text)):
        # if "." in word: print(word.isalpha())
        # if (word.lower() not in list_of_common_words and
        #         not word.isnumeric() and len(word) > 3):
        # print(word.strip(), "\n")
        if i % 2 == 0 and len(fragment) > 0:
            sentences.append(fragment.strip())
        else:
            sentences[-1] = sentences[-1] + fragment.strip()
    sentences = [frag for frag in sentences if len(frag) > 2]
    return sentences

top_sentences = {}
for sentence in eng_sentence_splitter(all_words):
    for top in top_words:
        if top in sentence:
            print(sentence)
            break


def main(argv):
    defined_word = argv[0]
    # chat = ChatLog()
    # print(locale.getpreferredencoding())
    # print(filename)
    # messenger(defined_word, chat)

    with open("cat-urban.json", "r") as definition_file:
        definitions = json.loads(definition_file.read())

    all_words = ""
    for n, definition in enumerate(definitions["list"]):
        # print(n," ", definition["definition"], "\n")
        all_words += definition["definition"] + " "

    list_of_common_words = ["that", "with", "the", "to", "and", "you", "of",
                            "not", "for", "them",
                            "have", "when", "out", "as", "in", "are", "they",
                            "their", "your", "who", "all"]
    most_words = []
    for word in re.split("[,. ]", all_words):
        # if "." in word: print(word.isalpha())
        if (word.lower() not in list_of_common_words and
                not word.isnumeric() and len(word) > 3 and "\n" not in word):
            # for letter in word:
            #     if word[0] in [".", ]
            most_words.append(word)
    # print(definitions)

    try:
        template = env.get_template("definition.html")
        output = (template.render(defined_word=defined_word))

        with open(f"Statistics_about_{defined_word}.html", 'wb') as f:
            f.write(output.encode("utf-8"))
    except exceptions.TemplateNotFound:
        print("Template not found")





if __name__  == "__main__":
    main(sys.argv[1:])
    # main()
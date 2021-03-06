import requests, json, re, sys, collections
import re
from jinja2 import exceptions, Environment, BaseLoader, FileSystemLoader, select_autoescape
from caching_utils import check_file_is_young
from caching_utils import get_from_api

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
        if each[0-len(string):] == string and each not in result:
            result.append(each)
    return result


def word_frequency(word_list: list):
    """
    Returns a dict of words and their frequency in a given list
    :param word_list:
    :return: Dict of word frequency
    """
    frequency = {}
    for word in word_list:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def top_x_words(frequency: dict, size: int) -> list:
    """
    Returns a list of the top x words, sorted by frequency, as a tuple: word, f
    requency, % of every word.
    :param frequency:
    :param size:
    :return:
    """
    top_words = []
    for i, word in enumerate(
            sorted(frequency, key=frequency.get, reverse=True)):
        if i < size:
            percent = frequency[word] / len(frequency) * 100
            top_words.append((word, frequency[word], str(round(percent, 2)) + "%"))
        else:
            break
    return top_words


def words_at_most(word_list: list, size: int) -> list:
    short_words = []
    for word in word_list:
        if len(word) <= size:
            short_words.append(word)
    return short_words


def words_at_least(word_list: list, size: int) -> list:
    long_words = []
    for word in word_list:
        if len(word) >= size:
            long_words.append(word)
    return long_words


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


def sentence_importance(sentences: list, word_list: list) -> dict:
    """
    Returns a dict of sentences and their importance (based on count of words in
    word_list contained within that sentence
    :param sentences: The sentences to analyse
    :param word_list: The words to a use in anaylsis
    :return: A dict of sentence => relative interest
    """
    interesting_sentences = {}
    for sentence in sentences:
        for word in word_list:
            if word in sentence:
                interesting_sentences[sentence] = interesting_sentences.get(
                    sentence, 0) + 1
    return interesting_sentences


def top_x_sentences(frequency: dict, size: int) -> list:
    """
    Returns a list of the top x words, sorted by frequency, as a tuple: word,
    frequency, % of words given that this sentence contains
    :param frequency:
    :param size:
    :return:
    """
    top_sentences = []
    for i, word in enumerate(
            sorted(frequency, key=frequency.get, reverse=True)):
        if i < size:
            percent = frequency[word] / size * 100
            top_sentences.append((word, frequency[word], str(round(percent, 2)) + "%"))
        else:
            break
    return top_sentences


def text_is_naughty(naughty_words: list, text: str) -> bool:
    """
    Return true if text contains naughty word from LDNOOBW list
    :param naughty_words: a list of words to search against
    :param text: text to search
    :return: boolean of naughtiness
    """
    # for word in text.split():
    #     if word.lower() in naughty_words:
    #         return True

    for naughty_word in naughty_words:
        re_pattern = f"\\b{naughty_word}"
        if re.search(re_pattern, text):
            return True
    return False


def analyse_definition(defined_word, definitions):
    naughty_words = []
    with open("word_lists/LDNOOBW_en.txt") as naughty_words_list:
        naughty_words = naughty_words_list.read().splitlines()

    list_of_common_words = ["type", "with", "the", "to", "and", "you", "of",
                            "not", "for", "them",
                            "have", "when", "out", "as", "in", "are", "they",
                            "their", "your", "who", "all"]
    with open("word_lists/google-10000-english-no-swears.txt", "r") as words:
        for line_num, line in enumerate(words):
            list_of_common_words.append(line.strip())
            if line_num > 100:
                break

    naughty_definitions = []
    clean_definitions = []
    all_words = ""
    sentences = []

    # loop over each definition
    for n, definition in enumerate(definitions["list"]):
        all_words += definition["definition"] + " "
        sentences.extend(eng_sentence_splitter(definition["definition"]))
        if text_is_naughty(naughty_words, definition["definition"]):
                naughty_definitions.append(definition["definition"])
        else:
            clean_definitions.append(definition["definition"])

    most_words = []
    for word in re.split("[,. ]", all_words):
        if (word.lower() not in list_of_common_words and
                not word.isnumeric() and len(word) >= 3 and "\n" not in word):
            most_words.append(word)

    top_10_words = top_x_words(word_frequency(most_words), 10)
    the_10_top_words = []
    for freq in top_10_words:
        the_10_top_words.append(freq[0])

    sentences_with_interest = sentence_importance(sentences, the_10_top_words)
    top_10_sentences = top_x_sentences(sentences_with_interest, 10)

    big_words = words_at_least(most_words, 7)
    small_words = words_at_most(most_words, 4)

    WordStuff = collections.namedtuple('Def',
                                       'word top_10_sentences top_10_words '
                                       'long short most_words def_count '
                                       'naughty_defs clean_defs')
    word_stuff = WordStuff(word=defined_word, top_10_sentences=top_10_sentences,
                           top_10_words=top_10_words,
                           long=words_at_least(most_words, 9),
                           short=words_at_most(most_words, 4),
                           most_words=most_words,
                           def_count=len(definitions["list"]),
                           naughty_defs=naughty_definitions,
                           clean_defs=clean_definitions
                           )
    return word_stuff


def main(argv):
    defined_word = argv[0]

    if check_file_is_young(f"json/{defined_word}.json"):
        try:
            file = open(f"json/{defined_word}.json", "r")
            definitions = json.load(file)
        except FileNotFoundError:
            print("Can't read from file system, getting directly")
            definitions = get_from_api(defined_word)
    else:
        print("cache too old")
        try:
            definitions = get_from_api(defined_word)
            try:
                with open(f"json/{defined_word}.json", "w") as file:
                    json.dump(definitions, file)
            except OSError:
                print("can't save cache")
            except json.JSONDecodeError:
                print("nothing to write")
        except requests.ConnectionError:
            return "Can't connect"

    # create the container of analysis only if the result set > 0
    if len(definitions['list']) > 0:
        word_data = analyse_definition(defined_word, definitions)
    else:
        print(f"There's no results found for ' {defined_word} ' on Urban Dictionary")
        return

    print("number of (useful) words: ", len(word_data.most_words))

    print("\nTop 10 Words by frequency")
    for freq in getattr(word_data, "top_10_words"):
        print(freq[0], freq[1], freq[2])

    print("\nSentences containing the top words\n")
    for interesting_sentence in getattr(word_data, "top_10_sentences"):
        print(interesting_sentence[0], interesting_sentence[1], interesting_sentence[2])

    print("\nEnding in Y\n")
    for word in words_ending_in(word_data.most_words, "y"):
        print(word)

    print("\nEnding in D\n")
    for word in words_ending_in(word_data.most_words, "d"):
        print(word)

    print("\nLong Words\n")
    for word in word_data.long:
        print(word)

    print("\nShort Words\n")
    for word in word_data.short:
        print(word)

    print("\nNaughty Definitions\n")
    print(f"Out of {word_data.def_count} definitions for {word_data.word}, "
          f"the following {len(word_data.naughty_defs)} are naughty:")
    for definition in word_data.naughty_defs:
        print("~~ " + definition + " /~~")

    print("\nClean Definitions\n")
    print(f"Out of {word_data.def_count} definitions for {word_data.word}, "
          f"the following {len(word_data.clean_defs)} are clean:")
    for definition in word_data.clean_defs:
        print("~~ " + definition + " /~~")


    try:
        template = env.get_template("definition.html")
        output = (template.render(data=word_data))

        with open(f"Statistics_about_{defined_word}.html", 'wb') as f:
            f.write(output.encode("utf-8"))
    except exceptions.TemplateNotFound:
        print("Template not found")


if __name__ == "__main__":
    main(sys.argv[1:])
    # main()

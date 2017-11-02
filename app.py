import requests, json, re, sys, collections
from jinja2 import exceptions, Environment, BaseLoader, FileSystemLoader, select_autoescape
from flask import Flask, request, render_template
from word_stats import *
from caching_utils import *

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)


@app.route('/')
def main():
    word = request.args.get("word", None)
    if word is None or len(word) == 0 or word.isspace():
        return "use /?word=[word]"

    defined_word=word
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

    all_words = ""

    for n, definition in enumerate(definitions["list"]):

        all_words += definition["definition"] + " "

    list_of_common_words = ["that", "with", "the", "to", "and", "you", "of",
                            "not", "for", "them",
                            "have", "when", "out", "as", "in", "are", "they",
                            "their", "your", "who", "all"]
    most_words = []
    for word in re.split("[,. ]", all_words):
        if (word.lower() not in list_of_common_words and
                not word.isnumeric() and len(word) > 3 and "\n" not in word):
            most_words.append(word)

    top_10_words = top_x_words(word_frequency(most_words), 10)
    the_10_top_words = []
    for freq in top_10_words:
        the_10_top_words.append(freq[0])

    sentences = eng_sentence_splitter(all_words)
    sentences_with_interest = sentence_importance(sentences, the_10_top_words)
    top_10_sentences = top_x_sentences(sentences_with_interest, 10)

    big_words = words_at_least(most_words, 7)

    small_words = words_at_most(most_words, 4)

    WordStuff = collections.namedtuple('Def',
                                       'word top_10_sentences top_10_words long short')
    word_stuff = WordStuff(word=defined_word, top_10_sentences=top_10_sentences,
                           top_10_words=top_10_words,
                           long=words_at_least(most_words, 9),
                           short=words_at_most(most_words, 4),
                           )
    try:
        template = env.get_template("definition.html")
        output = (template.render(data=word_stuff))
        try:
            with open(f"Statistics_about_{defined_word}.html", 'wb') as f:
                f.write(output.encode("utf-8"))
        except OSError:
            print("Can't write to file system")
        return output
    except exceptions.TemplateNotFound:
        print("Template not found")



if __name__ == '__main__':
    app.run()
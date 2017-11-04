from flask import Flask, request
from jinja2 import exceptions, Environment, BaseLoader, FileSystemLoader, select_autoescape
import json
import requests

from caching_utils import check_file_is_young, get_from_api
from word_stats import analyse_definition

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

    # create the container of analysis
    word_stuff = analyse_definition(defined_word, definitions)
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
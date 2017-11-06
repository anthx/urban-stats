from flask import Flask, request
from jinja2 import exceptions, Environment, BaseLoader, FileSystemLoader, select_autoescape
import json
import requests
import boto3

from caching_utils_aws import check_file_is_young
from caching_utils import get_from_api
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
    client = boto3.client('s3')
    resource = boto3.resource("s3")
    object_key = f'json/{defined_word}.json'
    if check_file_is_young(f"json/{defined_word}.json"):
        try:

            s3_object = resource.Object('urban-statistics', object_key).get()["Body"]
            definitions = json.load(s3_object)
        except FileNotFoundError:
            print("Can't read from file system, getting directly")
            definitions = get_from_api(defined_word)
    else:
        print("cache too old")
        try:
            definitions = get_from_api(defined_word)
            try:

                client.put_object(Body=bytes(json.dumps(definitions).encode()),
                                  Bucket='urban-statistics',
                                  Key=object_key)
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
        return output
    except exceptions.TemplateNotFound:
        print("Template not found")


if __name__ == '__main__':
    app.run()
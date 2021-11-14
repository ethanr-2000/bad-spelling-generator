from flask import Flask, render_template, make_response, request, send_from_directory
from flask_cors import CORS
from helpers.spell_bad import spell_bad
from helpers.util import load_pronunciation_dictionary, load_isle
import re

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

isleDict = load_isle()
pd = load_pronunciation_dictionary()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/favicon.ico")
def favicon():
    return send_from_directory('./static', 'favicon.ico')


@app.route("/spellbad", methods=['POST'])
def spellbad():
    words_list = re.findall(r"[\w']+|[.,!?; ]", request.json['text'])
    response = {"words": []}
    for word in words_list:
        if re.match(r"[.,!?; ]", word):
            response['words'].append({'badlySpelled': [word]})
            continue
        bad_spell_response = spell_bad(word, isleDict, pd)
        response['words'].append(bad_spell_response)
    return make_response(response, 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

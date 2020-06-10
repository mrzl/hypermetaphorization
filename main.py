from flask import Flask, render_template, request
from flask_socketio import SocketIO
import settings
from nltk.corpus import wordnet as wn


# "threading", "eventlet" or "gevent"
async_mode = 'threading'
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/', methods=['POST', 'GET'])
def do_wordnet():
    result = False
    result_synonym_list = []
    result_hyponym_list = []
    result_hypernym_list = []
    input_list = []
    if request.method == 'POST':
        input = request.form['input']
        input = input.split(' ')
        input_list = input
        for word in input:
            synonym_list = []
            hyponym_list = []
            hypernym_list = []
            syns = wn.synsets(word)
            for syn in syns:
                for synonym in syn.lemma_names():
                    synonym_list.append(synonym)
                hypos = syn.hyponyms()
                hypers = syn.hypernyms()
                for hypo in hypos:
                    for name in hypo.lemma_names():
                        hyponym_list.append(name)

                for hyper in hypers:
                    for name in hyper.lemma_names():
                        hypernym_list.append(name)

                synonym_list[:] = [s.replace('_', ' ') for s in synonym_list]
                hypernym_list[:] = [s.replace('_', ' ') for s in hypernym_list]
                hyponym_list[:] = [s.replace('_', ' ') for s in hyponym_list]

            synonym_list = list(sorted(set(synonym_list)))
            hypernym_list = list(sorted(set(hypernym_list)))
            hyponym_list = list(sorted(set(hyponym_list)))

            result_synonym_list.append([word] + synonym_list)
            result_hyponym_list.append([word] + hyponym_list)
            result_hypernym_list.append([word] + hypernym_list)

        result = True

    return render_template('index.html', result=result, input=input_list, synonyms=result_synonym_list, hypernyms=result_hypernym_list, hyponyms=result_hyponym_list)


if __name__ == "__main__":

    socketio.run(app, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
from flask import Flask, render_template, request,jsonify
from wordle import get_best_word, word_response

app = Flask(__name__)


@app.route("/wordle")
def wordle():
    return render_template('wordle.html')


@app.route("/wordlesolve", methods=['POST'])
def get_next_word():
    words = request.json['words']
    conditions = request.json['conditions']
    next_word = get_best_word(words, conditions)
    return jsonify(next_word)


@app.route("/wordlevbot")
def wordle_v_bot():
    return render_template('wordlecompetition.html')


@app.route("/wordlenextturn", methods=['POST'])
def next_turn():
    word = "".join(request.json['word']).lower()
    solution = request.json['win_inx']
    conditions = word_response(word, solution)
    if conditions is False:
        return jsonify(False)
    bot_word = get_best_word(request.json['botwords'], request.json['botconditions'])
    bot_conditions = word_response(bot_word, solution)
    return jsonify(conditions, bot_word, bot_conditions)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/sudoku")
def sudoku():
    return render_template('sudoku.html')


@app.route("/wordlehard")
def wordlehard():
    return render_template('wordlehard.html')


@app.route("/wordlehardnextturn", methods=['POST'])
def hard_next_turn():
    word = "".join(request.json['word']).lower()
    solution = request.json['win_inx']
    conditions = word_response(word, solution, "scrabble.json")
    if conditions is False:
        return jsonify(False)
    return jsonify(conditions)


app.run("127.0.0.1", 3000)


from boggle import Boggle
from flask import Flask, request, render_template, jsonify, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "seekret-est-shhhhhh"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/home')
def show_homepage():
    """ Displays the homepage, and selects the letters to be used"""

    session['game_board'] = boggle_game.make_board()
    return render_template('home.html')
 
@app.route('/game')
def show_gamepage():
    """renders the game page"""

    return render_template('game.html')

@app.route('/check-entry', methods=["POST"])
def check_entry():
    """Recieves a <word>
        POST request: data: {entry: <word>}
        sends the word and gameboard to be validated
        returns the result in a json dict
         """

    entry = request.json['entry']
    board = session['game_board']
    is_valid_word = boggle_game.check_valid_word(board, entry)
    return jsonify({'result': is_valid_word})

@app.route("/scores", methods=["POST"])
def post_score():
    """Receive score, update the playcount, check/update high score"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    playCount = session.get("playCount", 0)

    session['playCount'] = playCount + 1
    session['highscore'] = max(score, highscore)

    return jsonify(higherScore=score > highscore)

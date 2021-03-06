from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    def test_homepage(self):
        """Testing the homepage (This is the easy one)"""
        with app.test_client() as client:
            resp = client.get('/home')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Boggle', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_gamepage(self):
        """Testing the gamepage."""
        with app.test_client() as client:
            resp = client.get('/game')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Boggle!', html)
            self.assertIn('timerLabel', html)
            self.assertIn('board', session)

    def test_valid_word(self):
        """Testing a valid word by setting the gameboard to a known setup"""
        with app.test_client() as client:
            with client.session as session:
                session['board'] = [["V", "I", "D", "E", "O"],
                                    ["G", "A", "M", "E", "S"],
                                    ["A", "R", "E", "M", "Y"],
                                    ["L", "I", "F", "E", "A"],
                                    ["N", "D", "D", "O", "G"]]
                resp = self.client.post('/check-entry', json={'entry': 'MAGE'})
                self.assertEquals(resp.json['result'], 'ok')

    def test_invalid_word(self):
        """Testing a word that is not on the board"""
        with app.test_client() as client:
            client.get('/game')
            resp = client.post('/check-entry', json={'entry': 'hexakisoctahedron'})
            self.assertEquals(resp.json['result'],'not-on-board')

    def test_gibberish(self):
        """Testing a non-english word"""
        with app.test_client() as client:
            client.get('/game')
            resp = client.post('/check-entry', json={'entry': 'souvienes'})
            self.assertEquals(resp.json['result'], 'not-word')
from flask import Flask, request, render_template
from treys import Card, Evaluator

app = Flask(__name__)

class PokerDecisionMaker:
    def __init__(self):
        self.evaluator = Evaluator()
        self.hand = []
        self.table_cards = []
        self.pot_size = 0
        self.last_bet = 0

    def input_hand(self, card1, card2):
        self.hand = [Card.new(card1), Card.new(card2)]

    def input_table_cards(self, *cards):
        self.table_cards = [Card.new(card) for card in cards]

    def set_pot_size(self, amount):
        self.pot_size = amount

    def set_last_bet(self, amount):
        self.last_bet = amount

    def pot_odds(self):
        if self.last_bet == 0:
            return float('inf')
        return self.pot_size / self.last_bet

    def best_decision_pre_flop(self):
        hand_strength = self.evaluator.evaluate(self.hand, [])
        if hand_strength < 100:
            return "Raise"
        elif hand_strength < 200:
            return "Call" if self.pot_odds() > 2 else "Fold"
        else:
            return "Fold"

    def best_decision_post_flop(self):
        score = self.evaluator.evaluate(self.hand, self.table_cards)
        if score < 100:
            return "Bet"
        elif score < 200:
            return "Check or Call" if self.pot_odds() > 1.5 else "Fold"
        else:
            return "Fold"

@app.route('/', methods=['GET', 'POST'])
def index():
    decision = ""
    if request.method == 'POST':
        hand1 = request.form['hand1']
        hand2 = request.form['hand2']
        pot_size = int(request.form['pot_size'])
        last_bet = int(request.form['last_bet'])
        table_cards = request.form['table_cards'].split(',')

        poker_tool = PokerDecisionMaker()
        poker_tool.input_hand(hand1, hand2)
        poker_tool.set_pot_size(pot_size)
        poker_tool.set_last_bet(last_bet)
        poker_tool.input_table_cards(*table_cards)

        decision_pre_flop = poker_tool.best_decision_pre_flop()
        decision_post_flop = poker_tool.best_decision_post_flop()
        decision = f"Pre-Flop Decision: {decision_pre_flop}, Post-Flop Decision: {decision_post_flop}"

    return render_template('index.html', decision=decision)

if __name__ == '__main__':
    app.run(debug=True)

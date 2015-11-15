from apbj import apbj

__author__ = 'stick2020'


def test_card_properties():
    c = apbj.Card('clubs', 'ace')
    assert c.suite == 'clubs'
    assert c.value == 'ace'
    assert c.bj_value == 11
    assert c.name == 'ace of clubs'
    assert c.face_up == False
    c.face_up = True
    assert c.face_up == True
    c.bj_value = 1
    assert c.bj_value == 1


def test_deck_properties():
    d = apbj.Deck()
    assert len(d.cards) == 52
    clubs = 0
    diamonds = 0
    kings = 0
    for c in d.cards:
        if c.suite == 'clubs':
            clubs += 1
        if c.suite == 'diamonds':
            diamonds += 1
        if c.value == 'king':
            kings += 1
    assert clubs == 13
    assert diamonds == 13
    assert kings == 4


def test_bjshoe_properties():
    decks = [apbj.Deck(), apbj.Deck(), apbj.Deck()]

    bjshoe = apbj.BlackJackShoe(decks)
    assert len(bjshoe.active_pile) == 156
    bjshoe.draw(2)
    assert len(bjshoe.active_pile) == 154
    bjshoe.shuffle()
    assert len(bjshoe.active_pile) == 156


def test_hand_properties():
    decks = [apbj.Deck(), apbj.Deck(), apbj.Deck()]
    bjshoe = apbj.BlackJackShoe(decks)
    h = apbj.Hand(5.00)
    h.add_cards(bjshoe.draw(2))
    assert len(h.cards) == 2

    card_count = 2
    while h.bj_value < 21:
        h.add_cards(bjshoe.draw())
        card_count += 1
        assert len(h.cards) == card_count


def test_hand_blackjack():
    cards2 = [apbj.Card('clubs', 'ace'), apbj.Card('clubs', 'queen')]
    h2 = apbj.Hand(5.00)
    h2.add_cards(cards2)
    assert h2.blackjack == True

    cards3 = [apbj.Card('clubs', '9'), apbj.Card('clubs', 'queen')]
    h3 = apbj.Hand(5.00)
    h3.add_cards(cards3)
    assert h3.blackjack == False


def test_hand_bust():
    cards4 = [apbj.Card('clubs', '9'), apbj.Card('clubs', 'queen')]
    h4 = apbj.Hand(5.00)
    h4.add_cards(cards4)
    assert h4.is_bust() == False

    cards5 = [apbj.Card('clubs', '9'), apbj.Card('clubs', 'queen'), apbj.Card('clubs', 'king')]
    h5 = apbj.Hand(5.00)
    h5.add_cards(cards5)
    assert h5.is_bust() == True


def test_hand_aces():
    cards6 = [apbj.Card('clubs', 'ace'), apbj.Card('clubs', 'ace')]
    h6 = apbj.Hand(5.00)
    h6.add_cards(cards6)
    assert h6.bj_value == 12

    cards7 = [apbj.Card('clubs', 'ace'), apbj.Card('clubs', 'ace'), apbj.Card('clubs', '9')]
    h7 = apbj.Hand(5.00)
    h7.add_cards(cards7)
    assert h7.bj_value == 21

    cards8 = [apbj.Card('clubs', 'ace'), apbj.Card('clubs', 'ace'), apbj.Card('clubs', 'king'), apbj.Card('clubs', '3')]
    h8 = apbj.Hand(5.00)
    h8.add_cards(cards8)
    assert h8.bj_value == 15


def test_player_properties():
    cartman = apbj.Player('Cartman')
    assert cartman.bank == 50
    assert cartman.name == 'Cartman'

    cartman.bet(5)
    assert cartman.bank == 45

    king = apbj.Card('clubs', 'king')
    queen = apbj.Card('clubs', 'queen')
    cartman.hands[0].add_cards([king])
    cartman.hands[0].add_cards([queen])
    assert cartman.hands[0].bj_value == 20


def test_player_split_hand():
    kyle = apbj.Player('Kyle')
    kyle.bet(10)

    cards = [apbj.Card('clubs', 'king'),
             apbj.Card('hearts', 'king'),
             apbj.Card('spades', 'king'),
             apbj.Card('diamonds', 'king')]

    kyle.hands[0].add_cards([cards[0], cards[1]])
    kyle.hands[0].split(True)

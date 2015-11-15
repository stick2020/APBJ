import random
from operator import attrgetter

__author__ = 'stick2020'

class Card(object):
    def __init__(self, suite=None, value=None):
        self.value = value
        self.suite = suite
        self.face_up = False
        self.name = "{0} of {1}".format(self.value, self.suite)
        if self.value in ['10', 'jack', 'queen', 'king']:
            self.bj_value = 10
        elif self.value == 'ace':
            # will set bj_value to 1 when necessary
            self.bj_value = 11
        else:
            self.bj_value = int(self.value)

    def __repr__(self):
        return self.name


class Deck(object):
    def __init__(self):
        self.cards = []
        suites = ['clubs', 'spades', 'hearts', 'diamonds']
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'jack', 'queen', 'king']
        self.cards = [Card(s, v) for s in suites for v in values]


class BlackJackShoe(object):
    def __init__(self, decks):
        self.cards = [c for d in decks for c in d.cards]
        self.active_pile = self.cards[:]
        self.shuffle()

    def draw(self, num_of_cards=1):
        cards = []
        for i in range(num_of_cards):
            cards.append(self.active_pile.pop(num_of_cards))

        for c in cards:
            if c.bj_value >= 10:
                self.true_count -= 1
            elif int(c.value) < 7:
                self.true_count += 1

        return cards

    def shuffle(self):
        del self.active_pile[:]
        self.active_pile = self.cards[:]
        random.shuffle(self.active_pile)
        self.discard_pile = []
        self.true_count = 0


class Hand(object):
    def __init__(self, wager):
        self.cards = []
        self.bj_value = 0
        self.bust = False
        self.blackjack = False
        self.wager = wager
        self.insurance = False
        self.surrender = False

    def is_bust(self):
        return self.bust

    def show_hand(self):
        for c in self.cards:
            c.face_up = True

        return self.show_public_hand()

    def show_public_hand(self):
        face_up_cards = []
        for card in self.cards:
            if card.face_up == True:
                face_up_cards.append(card)
        return face_up_cards


    def add_cards(self, cards):
        self.cards.extend(cards)
        self.cards.sort(key=lambda c: c.bj_value)

        self.bj_value = 0
        for c in self.cards:
            if c.bj_value == 11 and self.bj_value > 10:
                c.bj_value = 1

            self.bj_value += c.bj_value

        if (len(self.cards) == 2) and (self.bj_value == 21):
           self.blackjack = True

        if self.bj_value > 21:
            self.bust = True


class Player(object):
    # Tracks Name, bank, hands, count (from his perspective) and playtype (aka decision making)
    def __init__(self, name, play_type='normal', bank=50.0):
        # Todo: need to allow player to play multiple positions
        # Todo: generate a unique player id
        self.name = name
        self.bank = bank
        self.hands = []
        self.shoe_count = 0
        self.hands_played = 0
        self.rounds_played = 0
        #self.play_type = PlayType(play_type)

    def __repr__(self):
        return self.name

    def bet(self, amt):
        del self.hands[:]
        if (amt < self.bank) and (amt > 0):
            self.bank -=  amt
            self.hands.append(Hand(amt))

    def hit(self, hand):
        # Todo: implement player.hit()
        pass

    def split(self, hand):
        # Todo: implement player.split()
        pass

    def double(self, hand):
        # Todo: implement player.double()
        pass

    def surrender(self):
        # Todo: implement player.surrender()
        pass

    def add_funds(self, amt):
        self.bank += amt


class PlayType(object):
    Play_Type = ['normal', 'aggressive', 'random', 'conservative']

    def hit_or_stay(self, play_type, dealer_hand, player_hand=None):

        if (int(dealer_hand.show_public_hand()[0].value) in [6, 5, 4]) and player_hand.value > 11:
            return False


        if play_type == 'aggressive':
            if player_hand.value < 17:
                return True #hit
            else:
                return False #stay
        elif play_type == 'random':
            # todo implement random hit/stay for values under 17
            if player_hand.value < 12:
                return True #hit
            else:
                return False #stay

        elif play_type == 'conservative':
            if player_hand.value < 12:
                return True #hit
            else:
                return False #stay

        else: #normal play_type
            if player_hand.value < 15:
                return True #hit
            else:
                return False #stay


    def split(self, cards):
        pass

    def double_down(self, cards):
        pass


# =============================================================================
class BlackJack(object):
    def __init__(self, deck):
        self.round = []
        self.deck = deck
        self.active_players=[]
        self.bank = 1000.00


    def phase_0(self, players):
        # add or remove players to start round
        self.add_players(players)

    def phase_1(self):
        # bet phase
        print '-'*40
        print 'start of phase_1 (bet)'
        for player in self.active_players:
            player.bet(1.0)
            #print "Player {} is betting 1.0".format(player.name)
            #print "Player {} bank is {}".format(player.name, player.bank)

    def phase_2(self):
        # deal phase
        print '-'*40
        print 'start of phase_2 (deal)'
        for counter in range(2):
            for player in self.active_players:
                player.hand.add_card(self.deck.draw()[0])
                if len(player.hand.cards) == 2:
                    player.hand.cards[1].face_up = True
                    #print "Public hand for {0}: {1}".format(player.name, player.hand.show_public_hand()[0].value)
                    #print "Full hand for {0}: {1}, {2}".format(player.name, player.hand.show_hand()[0].value, player.hand.show_hand()[1].value)

    def phase_3(self):
        # hit/stay phase
        # player doubles, splits or surrenders
        print '-'*40
        print 'start of phase_3 (hit/stay)'
        for player in self.active_players:
            print "="*20
            print "Player: {}".format(player.name)
            print "Starting hand value is: {}".format(str(player.hand.value))

            # dealer has blackjack
            if player.hand.value == 21:
                player.hand.blackjack = True
                if player.name == 'dealer':
                    print "Dealer has blackjack"
                    break

            # player hit/stay
            if player.name != 'dealer':
                while True:
                    if player.hit_or_stay():
                        print "Hitting..."
                        player.hand.add_card(self.deck.draw()[0])
                        print "Hand value is {}".format(player.hand.value)
                    else:
                        break
            else:
                # dealer hit/stay
                while True:
                    if player.hit_or_stay(dealer=True):
                        print "Hitting for dealer..."
                        player.hand.add_card(self.deck.draw()[0])
                        print "Hand value is {}".format(player.hand.value)
                    else:
                        break
            print "Final hand value is {}".format(player.hand.value)


    def phase_4(self):
        # reconcile all hands
        print '-'*40
        print 'start of phase_4 (bust)'
        for player in self.active_players:
            print "*"*20

            if (not(player.hand.is_bust()) and (player.name != 'dealer')):
                print "Player: {}".format(player.name)
                print "player hand value is {}".format(player.hand.value)
            else:
                print "player {} busted".format(player.name)

    def phase_5(self):
        # reconcile wagers
        print '-'*40
        print 'start of phase_5 (pay out)'
        for player in self.active_players:
            print '-'*20

            # collect busted player funds
            if (player.hand.is_bust()) and (player.name != 'dealer'):
                self.add_funds(player.hand.wager)
                print "Collecting busted player {} bet".format(player.name)
                print "session bank is: {}".format(self.bank)
                continue

            if player.name != 'dealer':
                # dealer bust. pay all unbusted player
                if self.active_players[-1].hand.is_bust():
                    if not(player.hand.is_bust()):
                        player.add_funds(player.hand.wager*2)
                        self.withdraw(player.hand.wager)
                        print "dealer busts. paying: {}".format(player.name)
                        print "Player bank is: {}".format(player.bank)
                        print "session bank is: {}".format(self.bank)
                        continue

                if player.hand.value > self.active_players[-1].hand.value:
                    # player beats dealer. pay player
                    player.add_funds(player.hand.wager*2)
                    self.withdraw(player.hand.wager)
                    print "player {} wins".format(player.name)
                    print "Player bank is: {}".format(player.bank)
                    print "session bank is: {}".format(self.bank)
                    continue

                if player.hand.value < self.active_players[-1].hand.value:
                    # dealer beats player
                    self.add_funds(player.hand.wager)
                    print "player {} loses".format(player.name)
                    print "Player bank is: {}".format(player.bank)
                    print "session bank is: {}".format(self.bank)
                    continue

                # push with dealer.  add bet back to player bank
                player.add_funds(player.hand.wager)
                print "player {} pushes".format(player.name)
                print "Player bank is: {}".format(player.bank)
                print "session bank is: {}".format(self.bank)



    def phase_6(self):
        # place cards in discard pile.
        # determine if we need to shuffle
        # reset round if shuffle
        # print player banks
        for player in self.active_players:
            player.hand.reset()
            player.hand.wager = 0.00

        print "Cards left in shoe: {}".format(len(self.deck.active_pile))
        if len(self.deck.active_pile) < 50:
            print "less than 50 cards in shoe.  SHUFFLING"
            self.deck.shuffle()

        for p in self.active_players:
            print "{0} has ${1}".format(p.name, p.bank)

        del self.active_players[:]

    def add_players(self, list_of_players):
        for player in list_of_players:
            self.add_player(player)

    def add_player(self, player):
        self.active_players.append(player)

    def withdraw(self, wager):
        self.bank -= wager

    def add_funds(self, wager):
        self.bank += wager





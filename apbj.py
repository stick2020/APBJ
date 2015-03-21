import random

__author__ = 'stick2020'


# =============================================================================
class Card(object):
    def __init__(self, suite=None, value=None):
        self.value = value
        self.suite = suite
        self.face_up = False
        self.name = "{0} of {1}".format(self.value, self.suite)


# =============================================================================
class Deck(object):
    def __init__(self):
        self.cards = [] # subclass should populate self.cards
        self.discard_pile = []
        self.true_count = 0

    def shuffle(self):
        self.active_pile = self.cards[:]
        random.shuffle(self.active_pile)
        self.true_count = 0

    def draw(self, num_of_cards=1):
        cards = [self.active_pile.pop() for n in range(1, num_of_cards+1)]
        return cards

    def discard(self, card):
        self.discard_pile.append(card)

    def _set_shuffle_point(self, percentage=66):
        pass


# =============================================================================
class StandardDeck(Deck):
    def __init__(self):
        super(StandardDeck, self).__init__()
        suites = ['clubs', 'spades', 'hearts', 'diamonds']
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'jack', 'queen', 'king']
        self.cards = [Card(s, v) for s in suites for v in values]
        self.shuffle()


# =============================================================================
class Shoe(Deck):
    def __init__(self, list_of_decks):
        super(Shoe, self).__init__()
        self.cards = [c for d in list_of_decks for c in d.cards]
        self.shuffle()


# =============================================================================
class BlackJackShoe(Shoe):
    def __init__(self, decks):
        super(BlackJackShoe, self).__init__(decks)
        self.true_count = 0

    def draw(self, num_of_cards=1):
        cards = super(BlackJackShoe, self).draw()
        for c in cards:
            if c.value == ('king'):
                self.true_count -= 1
            elif c.value == ('queen'):
                self.true_count -= 1
            elif c.value == ('jack'):
                self.true_count -= 1
            elif c.value == ('ace'):
                self.true_count -= 1
            elif int(c.value) == 10:
                self.true_count -= 1
            elif int(c.value) < 7:
                self.true_count += 1
        return cards

    def shuffle(self):
        super(BlackJackShoe, self).shuffle()
        self.true_count = 0

# =============================================================================
class Hand(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        self.value = 0
        self.bust = False
        self.blackjack = False
        self.wager = 0.00

    def is_bust(self):
        return self.bust

    def show_hand(self):
        return self.cards

    def show_public_hand(self):
        face_up_cards = []
        for card in self.cards:
            if card.face_up == True:
                face_up_cards.append(card)
        return face_up_cards


    def add_card(self, card, face_up=False):
        self.cards.append(card)
        if card.value in ['jack', 'queen','king']:
            self.value += 10
        elif card.value == 'ace':
            if self.value > 10:
                self.value += 1
            else:
                self.value += 11
        else:
            self.value += int(card.value)

        if (len(self.cards) == 2) and (self.value == 21):
           self.blackjack = True

        if self.value > 21:
            self.bust = True


# =============================================================================
class Player(object):
    def __init__(self, name, play_type='normal', bank=50.0):
        self.name = name
        self.bank = bank
        self.hand = Hand()
        self.count = 0
        self.play_type = PlayType(play_type)

    def bet(self, amt):
        self.bank -=  amt
        self.hand.wager = amt

    def hit_or_stay(self, player):
        # simple rules
        if not(dealer):
            if self.hand.value < 15:
                return True # hit
            return False # stay
        else:
            # todo update dealer hit rules
            if self.hand.value < 17:
                return True
            else:
                return False

    def split(self):
        # todo
        pass

    def double(self):
        # todo
        pass

    def add_funds(self, amt):
        self.bank += amt


# =============================================================================
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
        self.round = 0
        self.deck = deck
        self.active_players=[]
        self.bank = 1000.00

    def phase_0(self, players):
        # add or remove players to round
        print '-'*40
        print 'start of phase_0 (add players)'
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


# =============================================================================
if __name__ == '__main__':
    decks = [StandardDeck() for d in range(1, 7)]
    shoe = BlackJackShoe(decks)
    rounds = 100

    session = BlackJack(shoe)

    players = [Player('stan'),
               Player('david'),
               Player('brooklyn'),
               Player('mimi'),
               Player('emma'),
               Player('josh'),
               Player('dealer')]

    for round in range(rounds):
         print "Round: {}".format(round)
         session.phase_0(players)
         session.phase_1()
         session.phase_2()
         session.phase_3()
         #session.phase_4()
         session.phase_5()
         session.phase_6()




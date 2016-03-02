# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
result_message = ''
score = 0
dealer = None
player = None
deck = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
BJ = 21
DEALER_FUSE = 17

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        # pos is the upper left corner of the card
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_string = " ".join([str(c) for c in self.cards])
        return "Hand contains " + card_string

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        val = sum([VALUES[c.get_rank()] for c in self.cards])
        if val+10<=BJ and "A" in [c.get_rank() for c in self.cards]:
            return val+10
        return val
    
    def is_busted(self):
        return self.get_value() > BJ

    def draw(self, canvas, pos):
        # pos is the position of the upper left corner of the leftmost card
        for ind, card in enumerate(self.cards):
            card.draw(canvas, [pos[0] + ind * (CARD_SIZE[0]+10), pos[1]])
         
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        card_string = " ".join([str(c) for c in self.cards])
        return "Deck contains " + card_string

#define event handlers for buttons
def deal():
    global outcome, in_play, dealer, player, deck, result_message, score

    # your code goes here
    if in_play:
        score -= 1
        
    # init and shuffle deck
    deck = Deck()
    deck.shuffle()
    
    # init dealer and player
    dealer = Hand()    
    player = Hand()
    
    # deal two cards to both dealer and player in turn
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    # init message
    outcome = "Hit or stand?"
    result_message = ""
    
    in_play = True

def hit():
    global in_play, score, outcome, result_message
    
    if not in_play:
        return
    
    # if the hand is in play, hit the player
    player.add_card(deck.deal_card())
    if player.is_busted():
        # if busted, assign a message to outcome, update in_play and score
        in_play = False
        score += -1
        outcome = "New deal?"
        result_message = "You lose."
       
def stand():
    global in_play, score, outcome, result_message
    
    if not in_play:
        return
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer.get_value() < DEALER_FUSE:
        dealer.add_card(deck.deal_card()) 

    # assign a message to outcome, update in_play and score
    in_play = False
    outcome = "New deal?"
    if dealer.is_busted() or dealer.get_value() <  player.get_value():
        score += 1
        result_message = "You win."
    else:
        score -= 1
        result_message = "You lose."


# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    # draw player
    canvas.draw_text("Player", [70,335], 24, "Black")
    player.draw(canvas, [70, 360])
    canvas.draw_text(outcome, [150, 335], 24, "Blue")
    
    # draw dealer
    canvas.draw_text("Dealer", [70,155], 24, "Black")
    dealer.draw(canvas, [70, 180])
    canvas.draw_text(result_message, [150, 155], 24, "Blue")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [70 + CARD_BACK_CENTER[0], 180 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
          
    # draw title and score
    canvas.draw_text("Blackjack", [80, 80], 30, "Blue")
    canvas.draw_text("Score " + str(score), [300,80],24,"Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 500, 500)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric

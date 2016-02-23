# implementation of card game - Memory

import simplegui
import random

CAN_SIZE = [300, 450]
GRID_DIM = [4, 4]
GRID_SIZE = [CAN_SIZE[0]/GRID_DIM[0], CAN_SIZE[1]/GRID_DIM[1]]
PADDING = 4

IMG_BACK = simplegui.load_image("http://i.imgur.com/NO7OHg3.png")
IMG_BACK_SIZE = [150, 223]

NUM_IMAGE = simplegui.load_image("http://i.imgur.com/nS2rGHY.png")
NUM_SIZES = [(203,528,126,140),
             (65,69,100,138),
             (200,69,120,138),
             (348,69,120,138),
             (56,226,112,132),
             (198,230,120,140),
             (349,227,118,142),
             (62,384,120,136),
             (201,387,122,142),
             (350,386,116,140)]

cards = []
turns = 0
exposed = 0
exposed_1 = -1
exposed_1 = -2

# draw lines
def draw_lines(canvas):
    # horizontal lines
    for i in range(1,GRID_DIM[1]):
        canvas.draw_line((0,GRID_SIZE[1]*i),(CAN_SIZE[0],GRID_SIZE[1]*i),1,"White")
        
    # vertical lines
    for i in range(1,GRID_DIM[0]):
        canvas.draw_line((GRID_SIZE[0]*i,0),(GRID_SIZE[0]*i,CAN_SIZE[1]),1,"White")

# calculate card drawing size to fit the grid better
def calculate_card_size(image_size):
    scale_hor = float(GRID_SIZE[0])/image_size[0]
    scale_ver = float(GRID_SIZE[1])/image_size[1]
    if scale_ver < scale_hor:
        return [image_size[0]*GRID_SIZE[1]/image_size[1],GRID_SIZE[1]-PADDING]
    else:
        return [GRID_SIZE[0]-PADDING, image_size[1]*GRID_SIZE[0]/image_size[0]]
    
# draw single card which is a tuple of (index, value, exposed)
def draw_single_card(canvas, card):
    cen_dst = [(card[0]%GRID_DIM[0])*GRID_SIZE[0]+GRID_SIZE[0]//2, 
               (card[0]//GRID_DIM[0])*GRID_SIZE[1]+GRID_SIZE[1]//2]
    if card[2]: # exposed, draw number
        cen_src = [NUM_SIZES[card[1]][0], NUM_SIZES[card[1]][1]]
        size_src = [NUM_SIZES[card[1]][2], NUM_SIZES[card[1]][3]]
        card_size = calculate_card_size(size_src)
        canvas.draw_image(NUM_IMAGE,
                         cen_src,
                         size_src,
                         cen_dst,
                         card_size)
    else: # draw card back
        size_src = [IMG_BACK_SIZE[0]/2, IMG_BACK_SIZE[1]/2]
        card_size = calculate_card_size(size_src)
        canvas.draw_image(IMG_BACK, 
                          [IMG_BACK_SIZE[0]/2, IMG_BACK_SIZE[1]/2],
                          IMG_BACK_SIZE,
                          cen_dst,
                          card_size)

# draw cards
def draw_cards(canvas):
    for card in cards:
        draw_single_card(canvas, card)
            
# helper function to initialize globals
def new_game():
    global cards, turns, exposed, exposed_1, exposed_2, GRID_SIZE
    turns = 0
    exposed = 0
    exposed_1 = -1
    exposed_2 = -1
    cards = []
    GRID_SIZE = [CAN_SIZE[0]/GRID_DIM[0], CAN_SIZE[1]/GRID_DIM[1]]
    
    # init cards
    total_pairs = GRID_DIM[0] * GRID_DIM[1] // 2
    half_targets = range(10)*(total_pairs//10) + range(1,total_pairs%10+1)
    targets = half_targets + half_targets
    random.shuffle(targets)
    for i in range(len(targets)):
        cards.append([i, targets[i], False])
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, exposed_1, exposed_2, turns
    card_index = pos[0]//GRID_SIZE[0] + pos[1]//GRID_SIZE[1]*GRID_DIM[0]
    if not cards[card_index][2]:
        cards[card_index][2] = True
        if exposed == 0:
            exposed = 1
            exposed_1 = card_index
        elif exposed == 1:
            exposed = 2
            exposed_2 = card_index            
            turns = turns+1
        else:
            if cards[exposed_1][1] != cards[exposed_2][1]:
                # flip back in pairing fails
                cards[exposed_1][2] = False
                cards[exposed_2][2] = False
            exposed = 1
            exposed_1 = card_index
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    draw_lines(canvas)
    draw_cards(canvas)
    label.set_text("Turns = " + str(turns))

def horizontal_handler(text):
    try:
        hor = int(text)
        if hor>0:
            GRID_DIM[0] = hor
            new_game()
    except:
        print "invalid input"
       
def vertical_handler(text):
    try:
        ver = int(text)
        if ver>0:
            GRID_DIM[1] = ver
            new_game()
    except:
        print "invalid input"

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CAN_SIZE[0], CAN_SIZE[1])
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# set dimension
frame.add_label("")
frame.add_label("")
frame.add_label("Grid: %d x %d" % (GRID_DIM[0], GRID_DIM[1]))
frame.add_input("Set horizontal:", horizontal_handler, 100)
frame.add_input("Set vertical:", vertical_handler, 100)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric

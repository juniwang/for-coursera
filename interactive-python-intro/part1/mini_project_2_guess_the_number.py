# import required modules
import simplegui
import random
import math

# initialize global variables
secret_number = 0
attempts_left = 0

# the secret_number is in range [range_low, range_high) 
range_low = 0
range_high = 100

# helper function to show game over message and start a new game    
def game_over():
    # the game is over
    print "You have no more attempts. Sorry, the game is over"
        
    # start a new game
    new_game()
        
# helper function to start and restart the game
def new_game():
    global secret_number, attempts_left, range_low, range_high

    # set secret_number for a new game
    secret_number = random.randrange(range_low, range_high)
    
    # set max attemps allowed for the new game
    attempts_left = int(math.ceil(math.log(range_high - range_low + 1, 2)))
    
    print "\nNew game started."
    print "The secret number in in range [%d,%d)." % (range_low, range_high)
    print "You can try up to %d times." % attempts_left

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # set the new range
    global range_low, range_high
    range_low = 0
    range_high = 100
    
    # restart the game
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    # set the new range
    global range_low, range_high
    range_low = 0
    range_high = 1000
    
    # restart the game
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global secret_number, attempts_left, range_low, range_high
    
    try:
        # convert input guess str to int
        guess_int = int(guess)
        print "\nGuess was", guess
        
        # deduce the attempts_count
        attempts_left = attempts_left - 1
        
        # compare the guess with the secret number
        if guess_int == secret_number:
            print "Congratulations! It's correct!"
            new_game()
        elif attempts_left == 0:
            game_over()
        elif guess_int > secret_number:
            print "Lower"
            print "The remaining attempts is", attempts_left
        else:
            print "Higher"
            print "The remaining attempts is", attempts_left
            
    except:
        print "\nThe input is invalid."
        print "Please guess a number in range [%d, %d)" % (range_low, range_high)
        
        # deduce the attempts_count also
        attempts_left = attempts_left - 1
        if attempts_left == 0:
            game_over()
        else:
            print "The remaining attempts is", attempts_left
    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200) 

# add controls to frame and register event handlers for control elements
frame.add_button("Range is [0,100)", range100)
frame.add_button("Range is [0,1000)", range1000)
frame.add_input("Guess", input_guess, 100)

# start frame
frame.start()

# call new_game 
new_game()

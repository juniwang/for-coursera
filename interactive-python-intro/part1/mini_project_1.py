# Code for Mini-project # 1 - Rock-paper-scissors-lizard-Spock
import random

def name_to_number(name):
    """converts the string name into a number"""
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "name is not valid"

def number_to_name(number):
    """converts a number into the string name"""
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "number is not valid"

def rpsls(player_choice):
    """The game rock-paper-scissors-lizard-spock"""
    print ""
    
    # user choice
    print "Player chooses", player_choice
    player_number = name_to_number(player_choice)
    
    # computer choice
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses", comp_choice
    
    # compute the difference 
    difference = (comp_number - player_number) % 5
    if difference == 0:
        print "Player and computer tie!"
    elif difference < 3:
        print "Computer wins!"
    else:
        print "Player wins!"
    
# test the game
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

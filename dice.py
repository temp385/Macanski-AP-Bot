import random
from replit import db

# Dice Roll Minigame

def roll_1d6 ():
    dice = random.randint(1, 6)
    return dice

def player_roll ():
    output_msg = "You throw the dice."
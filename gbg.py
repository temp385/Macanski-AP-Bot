import random
from replit import db

# Galactic Battleship Game

def create_GBG_array(board_size, enemy_ships):
    if "GBG_board" not in db.keys():
        db["GBG_board"] = ""
    if "GBG_mask" not in db.keys():
        db["GBG_mask"] = ""
    if "GBG_mask" not in db.keys():
        db["GBG_dimension"] = ""
    if board_size.isnumeric():
        board_len = int(board_size)**2
        GBG_board="0"*(board_len)
        db["GBG_mask"] = GBG_board
        db["GBG_dimension"] = board_size
        GBG_board_arr = list(GBG_board)
        ship_locations_arr = random.sample(range(board_len), int(enemy_ships))
        for ship in ship_locations_arr:
            GBG_board_arr[ship] = "1"
        GBG_board = "".join(map(str, GBG_board_arr))
        db["GBG_board"] = GBG_board
        print(db["GBG_mask"])
        print(db["GBG_board"])
        print(db["GBG_dimension"])
    output = "New board created, dimention " + str(board_size) + " with " + str(enemy_ships) + " targets."
    return output

def show_GBG_grid():
    grid_icons=[":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:"]
    output=":stop_button:"
    max_dimension = int(db["GBG_dimension"])
    x_dimension = 0
    y_dimension = 0
    while x_dimension < max_dimension:
        output+=grid_icons[x_dimension]
        x_dimension+=1
    x_dimension = 0
    while y_dimension < max_dimension:
        output+="\n" + grid_icons[y_dimension]
        while x_dimension < max_dimension:
            output+=":blue_circle:"
            x_dimension+=1
        x_dimension=0
        y_dimension+=1
    return output
    

        
def get_user_GBGT(user_id):
    output = "unknown error"
    if "user_GBGTs" in db.keys():
        user_list = db["user_IDs"]
        user_GBGTs = db["user_GBGTs"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_GBGTs[lookup_index]
        except ValueError:
            output = "You are not registered, you need to be registered to play Galactic Battleship Game, type `$ap register` to register."
    return output

def set_user_GBGT(user_id, new_GBGT):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_GBGTs = db["user_GBGTs"]
        try:
            lookup_index = user_list.index(user_id)
            user_GBGTs[lookup_index] = str(new_GBGT)
            db["user_GBGTs"] = user_GBGTs
            output = "new GBGT = " + str(new_GBGT)
        except ValueError:
            output = "Something bad happened"
    return output

def fix_GBGT():
    user_GBGTs = db["user_GBGTs"]
    user_APs = db["user_APs"]
    if len(user_GBGTs) < len(user_APs):
        user_GBGTs.append("0")
        db["user_GBGTs"] = user_GBGTs
        output = "GBGTs equalized with APs successfuly."
    else:
        output = "No action required."
    return output

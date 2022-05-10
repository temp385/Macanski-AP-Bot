from replit import db

def check_flavor(random_int, lookup_user, user_APs):
    output_msg = "0"
    if random_int == 385:
        output_msg = "You (" + lookup_user + ") have 4096 AP available... wait, that can't be right... let me check that again... right, you actually have " + user_APs + " AP available. Sorry for the mix up. Cosmic ray bit flip or something."
    elif random_int == 350:
        output_msg = "You (" + lookup_user + ") have $3.50... I mean, you have " + user_APs + " AP available."
    elif random_int == 106:
        output_msg = "Well, wouldn't you (" + lookup_user + ") like to know how much AP you have? Fine, I'll tell you. You have " + user_APs + " AP available. You're welcome..."
    elif random_int == 69:
        output_msg = "You (" + lookup_user + ") have " + user_APs + " AP available. But Red over there looks kind of sus."
    elif random_int == 500:
        output_msg = "You (" + lookup_user + ") have " + user_APs + " AP available. Toss a Celes to your Commander, O' Galaxy of Plenty."
    elif random_int == 600:
        output_msg = "You (" + lookup_user + ") have 0x00000000 ValueError at line 513, unknown reference 'v=anGy31iIkr8', retrying...\nYou (" + lookup_user + ") have " + user_APs + " AP available."
    elif random_int == 700:
        output_msg = "You (" + lookup_user + ") have " + user_APs + " AP available.\nMacanski AP bot - Keeping your points somewhat safe since 2021."
    elif random_int == 800:
        output_msg = "You (" + lookup_user + ") have " + user_APs + " AP available. Hmm... deja vu..."
    elif random_int == 900:
        output_msg = "You (" + lookup_user + ") have " + user_APs + " AP available. Hey, there are some secret commands, like '$ap changelog', give it a try."
    return output_msg

def wrong_flavor(random_int):
    if random_int == "1":
        output_msg = "Nope, try again..."
    elif random_int == "2":
        output_msg = "Incorrect."
    elif random_int == "3":
        output_msg = "Negative."
    elif random_int == "4":
        output_msg = "No go."
    elif random_int == "5":
        output_msg = "That's not it..."
    elif random_int == "6":
        output_msg = "Wrong."
    elif random_int == "7":
        output_msg = "Aaaaand... No."
    elif random_int == "8":
        output_msg = ":("
    elif random_int == "9":
        output_msg = "False"
    elif random_int == "10":
        output_msg = "AP bot is now sad :'("
    elif random_int == "11":
        output_msg = "[AP bot grabs pop-corn to watch your struggles]"
    elif random_int == "12":
        output_msg = "[AP bot is not amused]"
    elif random_int == "13":
        output_msg = ":x:"
    elif random_int == "14":
        output_msg = "<:epsilon:649520458932158474>"
    elif random_int == "15":
        output_msg = "<:def:571161665853456384><:eat:571161883361542164>"
    elif random_int == "16":
        output_msg = "<:blobcorn:845315181466222592>"
    elif random_int == "17":
        output_msg = ":crying_cat_face:"
    elif random_int == "18":
        output_msg = ":chart_with_downwards_trend:"
    elif random_int == "19":
        output_msg = ":broken_heart:"
    elif random_int == "20":
        output_msg = ":no_entry_sign:"
    else:
        output_msg = "0"
    return output_msg

def riddle_check(ans):
    if db['riddle_mode'] == "hardcode":
        if str(ans.lower()) == "E" or str(ans.lower()) == "E" or str(ans.lower()) == "E" or str(ans.lower()) == "E":
            return "1"
        else:
            return "0"
    elif db['riddle_mode'] == "softcode":
        riddle_answer = db['riddle_answer']
        if str(ans.lower()) == str(riddle_answer.lower()):
            return "1"
        else:
            return "0"

def riddle_read():
    if db['riddle_mode'] == "hardcode":
        riddle_text = """no riddle available in this mode.""" 
    elif db['riddle_mode'] == "softcode":
        riddle_text = db['riddle_text']
    return riddle_text

def riddle_author():
    if db['riddle_mode'] == "hardcode":
        author="<@353973336654479361>" # Macanski
        # author="<@301361809766744077>" # vampirewolf
        # author="<@732509287380942898>" # padfoot9445
        # author="<@252535294866358273>" # Alex (sheo)
        # author="<@610115754058055681>" # R.I.P
        # author="<@518761614825095168>" # sr.mad
        # author="<@865330803117522944>" # BunchofApples
        # author="<@541311774058741783>" # Matyo
        # author="<@247767336306737153>" # TheAndylorian
        # author="<@565668919604674570>" # gurren lagann
        # author="<@452188168704229388>" # Darksnauw
        # author="<@600709047850631207>" # Yuyuko
        # author="<@763145299669418094>" # Spidroxide
        # author="<@679312739591782401>" # player unknown
        # author="<@557916819654967296>" # ThSurgeCell
        # author="<@694482743664574534>" # Betto
    elif db['riddle_mode'] == "softcode":
        author = db['riddle_author']
    return author

def riddle_category():
    if db['riddle_mode'] == "hardcode":
        # category = "SA related"
        # category = "Cross-over"
        category = "Other"
        # category = "Retro"
        # category = "MEGA RIDDLE"
        # category = "Discord"
        # category = "I have no idea what this is..."
        # category = "undefined"
        # category = "Creepy"
        # category = "Tribute"
    elif db['riddle_mode'] == "softcode":
        category = db['riddle_category']
    return category

def riddle_status():
    if db["riddle_trigger"] == "armed":
        return "1"
    else:
        return "0"

def riddle_trigger():
    if db["riddle_trigger"] == "armed":
        db["riddle_trigger"] = "disarmed"
        reward = db["riddle_points"]
        return reward
    else:
        return "0"
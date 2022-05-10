from flask import Flask, render_template
from threading import Thread
from replit import db
import jinja_functions as JF



import datetime



app = Flask('')

@app.route('/')
def hello():
    user_APs = db["user_APs"]
    user_IDs = db["user_IDs"]
    user_supp_IDs = db["user_supp_ID"]
    usernames = db["usernames"]
    return render_template('index.html', user_APs=user_APs, user_IDs=user_IDs, user_supp_IDs=user_supp_IDs, usernames=usernames)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@app.route('/transactions')
def test():
    # output = "Trans. ID  | AP | code  | username         | support ID"
    output = ""
    if "trans_timestamp" in db.keys():
        trans_timestamp = db["trans_timestamp"]
        trans_user_id = db["trans_user_id"]
        trans_ap_cost = db["trans_ap_cost"]
        trans_reward_code = db["trans_reward_code"]
        user_IDs = db["user_IDs"]
        username_cache = db["usernames"]
        trans_num = len(trans_timestamp)
        trans_current = 0
        while trans_current < trans_num:
            s1 = str(trans_timestamp[trans_current])
            s2 = str(trans_ap_cost[trans_current])
            s3 = str(trans_reward_code[trans_current])
            try:
                # user_id = int(trans_user_id[trans_current])
                # lookup_index = user_IDs.index(user_id)
                # username = str(username_cache[lookup_index])
                username = str(username_cache[user_IDs.index(
                    int(trans_user_id[trans_current]))])
            except:
                username = JF.get_username_from_id(trans_user_id[trans_current])
            # username = get_username_from_id(trans_user_id[trans_current])
            supp_ID = JF.get_user_supp_ID(int(trans_user_id[trans_current]))
            output += "<tr><td>" + str(trans_current+1) + "</td><td>" + s1 + "</td><td>" + s2 + "</td><td>" + s3 + "</td><td>" + username + "</td><td>" + supp_ID + "</td></tr>"
            trans_current += 1
        output += ""
        # return output
    return render_template('transactions.html', output=output)

@app.route('/csv')
def csv():
    user_IDs = db["user_IDs"]
    user_supp_IDs = db["user_supp_ID"]
    usernames = db["usernames"]
    return render_template('csv.html', user_IDs=user_IDs, user_supp_IDs=user_supp_IDs, usernames=usernames)

@app.route('/statistics')
def statistics():
    user_APs = db["user_APs"]
    user_IDs = db["user_IDs"]
    user_supp_IDs = db["user_supp_ID"]
    # usernames = db["usernames"]
    riddle_text = db["riddle_text"]
    riddle_answer = db["riddle_answer"]
    riddle_category = db["riddle_category"]
    slot_play_count = db["slot_stats_spin_count"]
    slot_win_count = db["slot_stats_win_count"]
    slot_total_payout = db["slot_stats_payout_count"]
    slot_win_ratio = int((int(slot_win_count) / int(slot_play_count))*100)
    slot_payout_ratio = int((int(slot_total_payout) / int(slot_play_count))*100)
    registered_users = len(user_IDs)
    active_AP = 0
    no_support = 0
    temp_current = 0
    user_0 = 0 # 0 AP
    user_1 = 0 # 1-10
    user_2 = 0 # 11-20
    user_3 = 0 # 21-30
    user_4 = 0 # 31-40
    user_5 = 0 # 41-50
    user_6 = 0 # 51+
    while temp_current < registered_users:
        temp_AP = int(user_APs[temp_current])
        active_AP += int(user_APs[temp_current])
        if len(str(user_supp_IDs[temp_current])) <= 1:
            no_support += 1
        if temp_AP == 0:
            user_0 += 1
        elif temp_AP > 0 and temp_AP <= 10:
            user_1 += 1
        elif temp_AP > 10 and temp_AP <= 20:
            user_2 += 1
        elif temp_AP > 20 and temp_AP <= 30:
            user_3 += 1
        elif temp_AP > 30 and temp_AP <= 40:
            user_4 += 1
        elif temp_AP > 40 and temp_AP <= 50:
            user_5 += 1
        elif temp_AP > 50:
            user_6 += 1
        temp_current += 1
    return render_template('statistics.html',
                           registered_users=registered_users,
                           active_AP=active_AP,
                           no_support=no_support,
                           user_0=user_0, user_1=user_1, user_2=user_2, user_3=user_3,
                           user_4=user_4, user_5=user_5, user_6=user_6,
                           slot_play_count=slot_play_count,
                           slot_win_count=slot_win_count,
                           slot_total_payout=slot_total_payout,
                           slot_win_ratio=slot_win_ratio,
                           slot_payout_ratio=slot_payout_ratio,
                          riddle_text=riddle_text,
                          riddle_answer=riddle_answer,
                          riddle_category=riddle_category)
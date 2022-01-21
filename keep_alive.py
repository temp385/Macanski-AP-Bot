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
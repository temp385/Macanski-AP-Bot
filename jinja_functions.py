from replit import db
import os
import requests
import json
import time

def get_username_from_id(user_id):
    url_string = "https://discord.com/api/v8/users/" + str(user_id)

    auth_type = "Bot " + str(os.environ['TOKEN'])
    headers = {"Authorization": auth_type}
    response = requests.get(url_string, headers=headers)
    json_data = json.loads(response.text)
    print(str(json_data))
    time.sleep(1)
    # print(str(time.time()))
    return json_data["username"]

def get_user_supp_ID(user_id):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_supp_ID = db["user_supp_ID"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_supp_ID[lookup_index]
        except ValueError:
            output = "-1"
    return output
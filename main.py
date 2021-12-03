import discord
import os
import requests
import json
import time
import datetime
import random
import math
import custom_functions as CF
import asyncio
from replit import db
from keep_alive import keep_alive

client = discord.Client()
max_ap_alowed = 50
claim_timeout = 2419200 # 28 days

reward_code_list = ["GXAL", "GXEP", "GXZE", "GXIO",
                    "CR100", "CR250", "CR500",
                    "CL50", "CL150", "CL300",
                    "CC10", "CC50", "CC100",
                    "GC1", "GC3", "GC5",
                    "BPFIG", "BPCOR", "BPFRI",
                    "BPCRU", "BPBAT", "BPCAR",
                    "BPSUP", "BPGAL",
                    "INCR", "MODI", "CHIP", "CRED"]
reward_name_list = ["Alpha Galaxy (L9)", "Epsilon Galaxy (L9)", "Zeta Galaxy (L9)", "Iota Galaxy (L9)",
                    "100.000 credits", "250.000 credits", "500.000 credits",
                    "50 celestium", "150 celestium", "300 celestium",
                    "10 common chips", "50 common chips", "100 common chips",
                    "1 gold chips", "3 gold chips", "5 gold chips",
                    "1 fighter special BP", "1 corvette special BP", "1 frigate special BP",
                    "1 cruiser special BP", "1 battleship special BP", "1 carrier special BP",
                    "1 super carrier special BP", "1 galactic carrier special BP",
                    "1 increase chance CU lvl 5", "1 modify chance CU lvl 5", "1 chip reduction CU lvl 5",
                    "1 credits reduction CU lvl 5"]
reward_cost_list = [5, 10, 15, 20,
                    2, 5, 10,
                    4, 10, 20,
                    2, 10, 20,
                    10, 30, 50,
                    5, 10, 20,
                    25, 30, 40,
                    45, 50,
                    30, 20, 15, 10]


def show_rewards():
    output = "```css\nCode  | Reward name                      | Cost (AP)"
    reward_len = len(reward_code_list)
    # print(reward_len)
    reward_current = 0
    while reward_current < reward_len:
        s1 = str(reward_code_list[reward_current])
        s2 = str(reward_name_list[reward_current])
        s3 = str(reward_cost_list[reward_current])
        output += "\n" + f'{s1:<5}' + " | " + f'{s2:<32}' + " | " + f'{s3:<3}'
        reward_current += 1
    output += "```"
    # print(output)
    return output


def get_user_AP(user_id):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_APs = db["user_APs"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_APs[lookup_index]
        except ValueError:
            output = "You are not registered, you need to be registered and have some AP to claim rewards, type `$ap register` to register."
    return output

def get_user_CT(user_id):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_CTs = db["user_CTs"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_CTs[lookup_index]
        except ValueError:
            output = "You are not registered, you need to be registered and have some AP to claim rewards, type `$ap register` to register."
    return output

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


def get_reward_cost(reward_code):
    try:
        lookup_index = reward_code_list.index(reward_code)
        # print(lookup_index)
        output = reward_cost_list[lookup_index]
    except ValueError:
        output = "Invalid reward code, please try again..."
    return output

def get_reward_index(reward_code):
    try:
        lookup_index = reward_code_list.index(reward_code)
        output = lookup_index
    except ValueError:
        output = "Invalid reward code, please try again..."
    return output


def get_reward_name(reward_code):
    try:
        lookup_index = reward_code_list.index(reward_code)
        # print(lookup_index)
        output = reward_name_list[lookup_index]
    except ValueError:
        output = "Invalid reward code, please try again..."
    return output


def set_user_AP(user_id, new_AP):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_APs = db["user_APs"]
        try:
            lookup_index = user_list.index(user_id)
            user_APs[lookup_index] = str(new_AP)
            db["user_APs"] = user_APs
            output = "new AP = " + str(new_AP)
        except ValueError:
            output = "Something bad happened"
    return output

def set_user_CT(user_id, new_CT):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_CTs = db["user_CTs"]
        try:
            lookup_index = user_list.index(user_id)
            user_CTs[lookup_index] = str(new_CT)
            db["user_CTs"] = user_CTs
            output = "new CT = " + str(new_CT)
        except ValueError:
            output = "Something bad happened"
    return output


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


def is_admin(user_id):
    output = str(user_id) in os.environ['ADMIN']
    return output


# db user APs (user_id, user_APs)
# db pending transactions (transaction ID, user_id, user_APs)

def create_transaction(user_id, ap_cost, reward_code):
    new_transaction_id = int(time.time())
    output = "error"
    if "trans_timestamp" in db.keys():
        trans_timestamp = db["trans_timestamp"]
        trans_user_id = db["trans_user_id"]
        trans_ap_cost = db["trans_ap_cost"]
        trans_reward_code = db["trans_reward_code"]
        trans_timestamp.append(str(new_transaction_id))
        trans_user_id.append(str(user_id))
        trans_ap_cost.append(str(ap_cost))
        trans_reward_code.append(str(reward_code))
        db["trans_timestamp"] = trans_timestamp
        db["trans_user_id"] = trans_user_id
        db["trans_ap_cost"] = trans_ap_cost
        db["trans_reward_code"] = trans_reward_code
    else:
        db["trans_timestamp"] = [new_transaction_id]
        db["trans_user_id"] = [user_id]
        db["trans_ap_cost"] = [ap_cost]
        db["trans_reward_code"] = [reward_code]
    output = "```css\nTransaction ID: [" + str(new_transaction_id) + "] created.```"
    return output


def show_all_transactions():
    output = "```css\nTrans. ID  | AP | code  | username         | support ID"
    if "trans_timestamp" in db.keys():
        trans_timestamp = db["trans_timestamp"]
        trans_user_id = db["trans_user_id"]
        trans_ap_cost = db["trans_ap_cost"]
        trans_reward_code = db["trans_reward_code"]
        trans_num = len(trans_timestamp)
        trans_current = 0
        while trans_current < trans_num:
            s1 = str(trans_timestamp[trans_current])
            s2 = str(trans_ap_cost[trans_current])
            s3 = str(trans_reward_code[trans_current])
            username = get_username_from_id(trans_user_id[trans_current])
            supp_ID = get_user_supp_ID(int(trans_user_id[trans_current]))
            output += "\n" + f'{s1:<10}' + " | " + f'{s2:<2}' + " | " + f'{s3:<5}' + " | " + f'{username:<16}' + " | " + supp_ID
            trans_current += 1
        output += "```"
        return output
    else:
        return "Pending transactions list is empty."


def show_user_transactions(user_id):
    output = "Showing pending transactions for user " + get_username_from_id(user_id) + ":\n"
    output += "```css\nTrans. ID  | AP | code  | reward name"
    if "trans_timestamp" in db.keys():
        trans_timestamp = db["trans_timestamp"]
        trans_user_id = db["trans_user_id"]
        trans_ap_cost = db["trans_ap_cost"]
        trans_reward_code = db["trans_reward_code"]
        trans_num = len(trans_timestamp)
        trans_current = 0
        while trans_current < trans_num:
            if str(trans_user_id[trans_current]) == str(user_id):
                s1 = str(trans_timestamp[trans_current])
                s2 = str(trans_ap_cost[trans_current])
                s3 = str(trans_reward_code[trans_current])
                s4 = str(get_reward_name(trans_reward_code[trans_current]))
                # username = get_username_from_id(trans_user_id[trans_current])
                # output += s1 + " | " + s2 + " | " + s3 + "\n"
                output += "\n" + f'{s1:<10}' + " | " + f'{s2:<2}' + " | " + f'{s3:<5}' + " | " + s4
            trans_current += 1
        output += "```"
        return output
    else:
        return "Pending transactions list is empty."


def refund_transaction(user_id, transaction_id):
    if str(transaction_id) == "0":
        return "Refund error - please provide the 10-digit transaction ID."
    elif str(transaction_id).isnumeric():
        if len(str(transaction_id)) == 10:
            if "trans_timestamp" in db.keys():
                trans_timestamp = db["trans_timestamp"]
                if str(transaction_id) in str(trans_timestamp):
                    try:
                        lookup_index = trans_timestamp.index(transaction_id)
                    except ValueError:
                        lookup_index = 0
                    trans_user_id = db["trans_user_id"]
                    if str(user_id) == str(trans_user_id[lookup_index]):
                        trans_ap_cost = db["trans_ap_cost"]
                        trans_reward_code = db["trans_reward_code"]
                        removed_trans_timestamp = trans_timestamp.pop(lookup_index)
                        removed_trans_user_id = trans_user_id.pop(lookup_index)
                        removed_trans_ap_cost = trans_ap_cost.pop(lookup_index)
                        removed_trans_reward_code = trans_reward_code.pop(lookup_index)
                        db["trans_timestamp"] = trans_timestamp
                        db["trans_user_id"] = trans_user_id
                        db["trans_ap_cost"] = trans_ap_cost
                        db["trans_reward_code"] = trans_reward_code
                        user_list = db["user_IDs"]
                        user_APs = db["user_APs"]

                        current_CT = get_user_CT(user_id)
                        reward_index = get_reward_index(removed_trans_reward_code)
                        current_CT_array = current_CT.split(',')
                        current_CT_array[reward_index] = "0"
                        new_CT = ','.join(map(str, current_CT_array))
                        set_user_CT(user_id, new_CT)

                        lookup_index2 = user_list.index(user_id)
                        current_AP = int(user_APs[lookup_index2])
                        refund_AP = int(removed_trans_ap_cost)
                        final_AP = current_AP + refund_AP
                        user_APs[lookup_index2] = str(final_AP)
                        db["user_APs"] = user_APs
                        output = "```css\nTransaction ID: " + str(
                            removed_trans_timestamp) + " refunded successfully.\nAP amount refunded: " + str(
                            removed_trans_ap_cost) + " AP\n" + "New total AP available: " + str(final_AP) + " AP\n```"
                        return output
                    else:
                        return "Refund error - you can't refund other users transactions."
                else:
                    return "Refund error - transaction ID not found."
            else:
                return "Refund error - no transactions found (DB empty)."
        else:
            return "Refund error - transaction ID must be exactly 10 digits long (example: 1234567890)."
    else:
        return "Refund error - please provide the 10-digit transaction ID (no letters or other symbols)."


def close_transaction(transaction_id):
    if str(transaction_id) == "0":
        return "Close transaction error - please provide the 10-digit transaction ID."
    elif str(transaction_id).isnumeric():
        if len(str(transaction_id)) == 10:
            if "trans_timestamp" in db.keys():
                trans_timestamp = db["trans_timestamp"]
                if str(transaction_id) in str(trans_timestamp):
                    try:
                        lookup_index = trans_timestamp.index(transaction_id)
                    except ValueError:
                        lookup_index = 0
                    trans_user_id = db["trans_user_id"]
                    trans_ap_cost = db["trans_ap_cost"]
                    trans_reward_code = db["trans_reward_code"]
                    removed_trans_timestamp = trans_timestamp.pop(lookup_index)
                    removed_trans_user_id = trans_user_id.pop(lookup_index)
                    removed_trans_ap_cost = trans_ap_cost.pop(lookup_index)
                    removed_trans_reward_code = trans_reward_code.pop(lookup_index)
                    db["trans_timestamp"] = trans_timestamp
                    db["trans_user_id"] = trans_user_id
                    db["trans_ap_cost"] = trans_ap_cost
                    db["trans_reward_code"] = trans_reward_code
                    # user_list = db["user_IDs"]
                    # user_supp_ID = db["user_supp_ID"]
                    # lookup_index2 = user_list.index(int(removed_trans_user_id))
                    supp_ID = str(get_user_supp_ID(int(removed_trans_user_id)))
                    # supp_ID = str(user_supp_ID[lookup_index2])
                    # write to file
                    current_time = datetime.datetime.now()
                    record = str(current_time)
                    record += " | Transaction ID: " + str(removed_trans_timestamp)
                    record += " | User ID: " + str(removed_trans_user_id)
                    record += " | Username: " + get_username_from_id(removed_trans_user_id)
                    record += " | User support ID: " + str(supp_ID)
                    record += " | Reward code: " + str(removed_trans_reward_code)
                    record += " | Reward name: " + str(get_reward_name(removed_trans_reward_code))
                    record += " | Reward cost: " + str(removed_trans_ap_cost)
                    record += "\n"
                    f = open("closed_transactions.txt", "a")
                    f.write(record)
                    f.close()
                    output = "```css\nTransaction ID: " + str(
                        removed_trans_timestamp) + " closed successfully.\n\nUser ID: " + str(
                        removed_trans_user_id) + "\nUsername: " + get_username_from_id(
                        removed_trans_user_id) + "\nUser support ID: " + str(supp_ID) + "\nReward code: " + str(
                        removed_trans_reward_code) + "\nReward name: " + str(
                        get_reward_name(removed_trans_reward_code)) + "\nReward cost: " + str(
                        removed_trans_ap_cost) + " AP\n```"
                    return output
                else:
                    return "Close transaction error - transaction ID not found."
            else:
                return "Close transaction error - no transactions found (DB empty)."
        else:
            return "Close transaction error - transaction ID must be exactly 10 digits long (example: 1234567890)."
    else:
        return "Close transaction error - please provide the 10-digit transaction ID (no letters or other symbols)."


def add_user(new_user_id, new_user_supp_id):
    if new_user_supp_id == "0":
        # check user_id but no user_supp_id
        if "user_IDs" in db.keys():
            user_IDs = db["user_IDs"]
            user_APs = db["user_APs"]
            user_CTs = db["user_CTs"]
            user_supp_ID = db["user_supp_ID"]
            if new_user_id in user_IDs:
                lookup_index = user_IDs.index(new_user_id)
                if user_supp_ID[lookup_index] == "0":
                    return "User already registered, you should register your support ID to be eligible to redeem rewards."
                else:
                    return "User already fully registered."
            else:
                user_IDs.append(new_user_id)
                user_APs.append("0")
                user_CTs.append("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                user_supp_ID.append("0")
                db["user_IDs"] = user_IDs
                db["user_APs"] = user_APs
                db["user_supp_ID"] = user_supp_ID
                return "Thank you... New user registered, you are now eligible to be awarded AP, you should also register your support ID to be eligible to redeem rewards."
        else:
            db["user_IDs"] = [new_user_id]
            db["user_APs"] = ["0"]
            db["user_CTs"] = ["0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"]
            db["user_supp_ID"] = ["0"]
            return "Thank you... New user registered, you are now eligible to be awarded AP, you should also register your support ID to be eligible to redeem rewards."
    elif str(new_user_supp_id).isnumeric():
        if len(str(new_user_supp_id)) == 16:
            if "user_IDs" in db.keys():
                user_IDs = db["user_IDs"]
                user_APs = db["user_APs"]
                user_supp_ID = db["user_supp_ID"]
                if new_user_id in user_IDs:
                    lookup_index = user_IDs.index(new_user_id)
                    user_supp_ID[lookup_index] = new_user_supp_id
                    db["user_supp_ID"] = user_supp_ID
                    return "Support ID updated successfully."
                else:
                    user_IDs.append(new_user_id)
                    user_APs.append("0")
                    user_supp_ID.append(new_user_supp_id)
                    db["user_IDs"] = user_IDs
                    db["user_APs"] = user_APs
                    db["user_supp_ID"] = user_supp_ID
                    return "Thank you... New user and support ID registered successfully, you are now eligible to be awarded AP and redeem rewards."
            else:
                db["user_IDs"] = [new_user_id]
                db["user_APs"] = ["0"]
                db["user_supp_ID"] = [new_user_supp_id]
                return "Thank you... New user and support ID registered successfully, you are now eligible to be awarded AP and redeem rewards."
        else:
            return "Registration error - please check your support ID (should be 16 digits) and try again."
    else:
        return "Registration error - please check your support ID (should be 16 digits only, no letters or other symbols) and try again."


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.channel.type) == "private":
        print("DM attempt")
        f = open("dm_attempts.txt", "a")
        f.write(str(message.channel) + " - " + str(message.content))
        f.close()
        await message.channel.send("Please use the designated channel #bot-commands.")
        return

    if message.author.bot == True and message.author != client.user and message.content.startswith("$ap"):
        await message.channel.send("Sorry, I'm only allowed to interact with humans.")
        return

    elif message.content == "$ap slots":
        symbol = [":x:", ":tangerine:", ":lemon:", ":watermelon:", ":cherries:", ":bell:", ":gem:"]
        reel_1 = "2452153412343513412321624"
        reel_2 = "2432125231413216312341324"
        reel_3 = "4232131526314323131241242"
        d1 = random.randint(1, 23)
        d2 = random.randint(1, 23)
        d3 = random.randint(1, 23)
        output_msg = ":black_medium_square::question::question::question::black_medium_square:\n:arrow_forward::question::question::question::arrow_backward:\n:black_medium_square::question::question::question::black_medium_square:"
        # output_msg = ":question::question::question:"
        own_msg = await message.channel.send(output_msg)
        await asyncio.sleep(1)
        output_msg = ":black_medium_square:" + str(
            symbol[int(reel_1[d1 - 1])]) + ":question::question::black_medium_square:\n:arrow_forward:" + str(
            symbol[int(reel_1[d1])]) + ":question::question::arrow_backward:\n:black_medium_square:" + str(
            symbol[int(reel_1[d1 + 1])]) + ":question::question::black_medium_square:"
        # output_msg = str(symbol[d1]) + ":question::question:"
        await own_msg.edit(content=output_msg)
        await asyncio.sleep(1)
        output_msg = ":black_medium_square:" + str(symbol[int(reel_1[d1 - 1])]) + str(
            symbol[int(reel_2[d2 - 1])]) + ":question::black_medium_square:\n:arrow_forward:" + str(
            symbol[int(reel_1[d1])]) + str(
            symbol[int(reel_2[d2])]) + ":question::arrow_backward:\n:black_medium_square:" + str(
            symbol[int(reel_1[d1 + 1])]) + str(symbol[int(reel_2[d2 + 1])]) + ":question::black_medium_square:"
        # output_msg = str(symbol[d1]) + str(symbol[d2]) +":question:"
        await own_msg.edit(content=output_msg)
        await asyncio.sleep(1)
        output_msg = ":black_medium_square:" + str(symbol[int(reel_1[d1 - 1])]) + str(
            symbol[int(reel_2[d2 - 1])]) + str(
            symbol[int(reel_3[d3 - 1])]) + ":black_medium_square:\n:arrow_forward:" + str(
            symbol[int(reel_1[d1])]) + str(symbol[int(reel_2[d2])]) + str(
            symbol[int(reel_3[d3])]) + ":arrow_backward:\n:black_medium_square:" + str(
            symbol[int(reel_1[d1 + 1])]) + str(symbol[int(reel_2[d2 + 1])]) + str(
            symbol[int(reel_3[d3 + 1])]) + ":black_medium_square:"
        # output_msg = str(symbol[d1]) + str(symbol[d2]) + str(symbol[d3])
        await own_msg.edit(content=output_msg)
        if str(reel_1[d1]) == "6" and str(reel_2[d2]) == "6" and str(reel_3[d3]) == "6":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 60X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "5" and str(reel_2[d2]) == "5" and str(reel_3[d3]) == "5":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 40X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "4" and str(reel_2[d2]) == "4" and str(reel_3[d3]) == "4":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 20X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "3" and str(reel_2[d2]) == "3" and str(reel_3[d3]) == "3":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 10X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "2" and str(reel_2[d2]) == "2" and str(reel_3[d3]) == "2":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 10X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "1" and str(reel_2[d2]) == "1" and str(reel_3[d3]) == "1":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 10X"
            await own_msg.edit(content=output_msg)
        elif (str(reel_1[d1]) == "4" and str(reel_2[d2]) == "4") or (
                str(reel_1[d1]) == "4" and str(reel_3[d3]) == "4") or (
                str(reel_2[d2]) == "4" and str(reel_3[d3]) == "4"):
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 4X"
            await own_msg.edit(content=output_msg)
        elif str(reel_1[d1]) == "4" or str(reel_2[d2]) == "4" or str(reel_3[d3]) == "4":
            await asyncio.sleep(1)
            output_msg += "\nWINRAR!! 1X"
            await own_msg.edit(content=output_msg)
        else:
            await asyncio.sleep(1)
            output_msg += "\nBetter luck next time..."
            # output_msg = str(symbol[d1]) + str(symbol[d2]) + str(symbol[d3]) + "\nBetter luck next time..."
            await own_msg.edit(content=output_msg)
        # output_msg = ":lemon::cherries::watermelon::gem::popcorn:"
        # await message.channel.send(output_msg, delete_after=5)

    elif message.content == "$ap update user list" or message.content == "$ap uul":
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            if "user_IDs" in db.keys():
                user_list = []
                usernames = []
                user_list = db["user_IDs"]
                user_num = len(user_list)
                user_current = 0
                own_msg = await message.channel.send("Updating user list, please wait...\n0% done.")
                while user_current < user_num:
                    usernames.append(get_username_from_id(user_list[user_current]))
                    # if user_current % 5 == 0:
                    output_msg = "Updating user list, please wait...\n" + str(
                        math.floor(float(user_current / user_num) * 100)) + "% done"
                    await own_msg.edit(content=output_msg)
                    user_current += 1
                output_msg = "Updating user list, please wait...\n100% done"
                await own_msg.edit(content=output_msg)
                db["usernames"] = usernames
                output_msg = "Usernames updated successfully."
            else:
                output_msg = "Warning: user_IDs error."
        else:
            output_msg = "You are not authorized to do that."
        await message.channel.send(output_msg)


    elif message.content == "$ap list all users" or message.content == "$ap lau":
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            await message.channel.send("Fetching list, please wait...")
            user_list = []
            output_msg = 'List of users:\n'
            if "user_IDs" in db.keys():
                user_list = db["user_IDs"]
                user_APs = db["user_APs"]
                user_supp_ID = db["user_supp_ID"]
                username_cache = db["usernames"]
                user_num = len(user_list)
                user_current = 0
                output_msg += "```xl\nUserID (Discord)   |  AP | Support ID       | Username"
                while user_current < user_num:
                    s1 = str(user_list[user_current])
                    s2 = str(user_APs[user_current])
                    s3 = str(user_supp_ID[user_current])
                    if s3 == "0":
                        s3 = "N/A"
                    try:
                        username = str(username_cache[user_current])
                    except:
                        username = get_username_from_id(user_list[user_current])
                    # username = "<" + str(user_list[user_current]) + ">"
                    output_msg += "\n" + f'{s1:<18}' + " | " + f'{s2:>3}' + " | " + f'{s3:>16}' + " | \'" + username + "\'"
                    # output_msg += str(user_list[user_current]) + " (" + username + ") with " + str(user_APs[user_current]) + " AP and support ID " + user_supp_ID[user_current] + "\n"
                    user_current += 1
                    if user_current % 20 == 0:
                        output_msg += "\n```"
                        await message.channel.send(output_msg)
                        output_msg = "```xl\nUserID (Discord)   |  AP | Support ID       | Username"
                output_msg += "\n```"
        else:
            output_msg = "You are not authorized to do that."
        await message.channel.send(output_msg)

    elif message.content.startswith("$ap aword user"):
        # protected
        is_embed = False
        user_id = int(message.author.id)
        if is_admin(user_id):
            temp_str = message.content.split("$ap aword user ", 1)[1]
            try:
                lookup_user = int(temp_str.split()[0])
                # print(lookup_user)
                add_AP = temp_str.split()[1]
                try:
                    if int(add_AP) <= 1000 and int(add_AP) >= -1000:
                        if int(add_AP) != 0:
                            # print(add_AP)
                            output_msg = ''
                            if "user_IDs" in db.keys():
                                user_list = db["user_IDs"]
                                user_APs = db["user_APs"]
                                try:
                                    lookup_index = user_list.index(lookup_user)
                                    current_AP = user_APs[lookup_index]
                                    new_total_AP = int(current_AP) + int(add_AP)
                                    user_APs[lookup_index] = str(new_total_AP)
                                    db["user_APs"] = user_APs
                                    output_msg = "User <@" + str(
                                        user_list[lookup_index]) + "> has been awarded with `" + str(
                                        add_AP) + " AP`, resulting in total of `" + str(
                                        user_APs[lookup_index]) + " AP`."
                                    embed = discord.Embed()
                                    # embed.title = "AP bot"
                                    embed.color = 0x253473
                                    embed.add_field(name="AP reward issued", value=output_msg, inline=False)
                                    is_embed = True
                                    # await ctx.send(embed=embed)
                                except ValueError:
                                    output_msg = "`User " + str(lookup_user) + " not found.`"
                        else:
                            output_msg = "Error... haha, very funny... :|"
                    else:
                        output_msg = "Amount out of range, please enter a number between 1 and 1000 (or -1 and -1000 to remove APs).\nCredits to vampirewolf for playing with big numbers :P"
                except ValueError:
                    output_msg = "Error - please insert a valid numeric value argument [AP amoutn]"
                except IndexError:
                    output_msg = "Error - missing argument [AP amount]"
            except ValueError:
                output_msg = "Error - please insert a valid numeric value argument [user ID (Discord)]. Type `$ap list all users` to get the list."
            except IndexError:
                output_msg = "Error - missing argument [AP amount]"
        else:
            output_msg = "You are not authorized to do that."
        if is_embed == True:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(output_msg)

    elif message.content.startswith("$ap award user"):
        # protected
        is_embed = False
        user_id = int(message.author.id)
        if is_admin(user_id):
            temp_str = message.content.split("$ap award user ", 1)[1]
            try:
                lookup_user = int(temp_str.split()[0])
                # print(lookup_user)
                add_AP = temp_str.split()[1]
                try:
                    if int(add_AP) <= 1000 and int(add_AP) >= -1000:
                        if int(add_AP) != 0:
                            # print(add_AP)
                            output_msg = ''
                            if "user_IDs" in db.keys():
                                user_list = db["user_IDs"]
                                user_APs = db["user_APs"]
                                try:
                                    lookup_index = user_list.index(lookup_user)
                                    current_AP = user_APs[lookup_index]
                                    new_total_AP = int(current_AP) + int(add_AP)
                                    user_APs[lookup_index] = str(new_total_AP)
                                    db["user_APs"] = user_APs
                                    output_msg = "User <@" + str(
                                        user_list[lookup_index]) + "> has been awarded with `" + str(
                                        add_AP) + " AP`, resulting in total of `" + str(
                                        user_APs[lookup_index]) + " AP`."
                                    embed = discord.Embed()
                                    # embed.title = "AP bot"
                                    embed.color = 0x253473
                                    embed.add_field(name="AP reward issued", value=output_msg, inline=False)
                                    is_embed = True
                                    # await ctx.send(embed=embed)
                                except ValueError:
                                    output_msg = "`User " + str(lookup_user) + " not found.`"
                        else:
                            output_msg = "Error... haha, very funny... :|"
                    else:
                        output_msg = "Amount out of range, please enter a number between 1 and 1000 (or -1 and -1000 to remove APs).\nCredits to vampirewolf for playing with big numbers :P"
                except ValueError:
                    output_msg = "Error - please insert a valid numeric value argument [AP amoutn]"
            except ValueError:
                output_msg = "Error - please insert a valid numeric value argument [user ID (Discord)]. Type `$ap list all users` to get the list."
        else:
            output_msg = "You are not authorized to do that."
        if is_embed == True:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(output_msg)

    elif message.content == "$ap check":
        is_embed = False
        lookup_user = str(message.author.name)
        lookup_user_id = int(message.author.id)
        output_msg = 'unknown error'
        if "user_IDs" in db.keys():
            user_list = db["user_IDs"]
            user_APs = db["user_APs"]
            # user_CTs = db["user_CTs"]
            try:
                lookup_index = user_list.index(lookup_user_id)
                random_int = random.randint(0, 1000)
                available_ap = user_APs[lookup_index]
                # claims_string = user_CTs[lookup_index]
                # claims_array = claims_string.split(',')
                # print(claims_array)
                flavor = CF.check_flavor(random_int, lookup_user, available_ap)
                if flavor == "0":
                    output_msg = "You (" + lookup_user + ") have " + available_ap + " AP available."
                else:
                    output_msg = flavor
                embed = discord.Embed()
                embed.color = 0x253473
                embed.add_field(name="AP check", value=output_msg, inline=False)
                is_embed = True
                if int(available_ap) > 50:
                    output_note = "The maximum amount allowed to accumulate is " + str(
                        max_ap_alowed) + " AP, you should redeem a reward or two.\nOtherwise, your over the limit AP points will be lost."
                    embed.add_field(name="Note", value=output_note, inline=False)
            except ValueError:
                output_msg = "You are not registered, just type `$ap register` to register."
        if is_embed == True:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(output_msg)

    elif message.content.startswith("$ap register"):
        user_id = int(message.author.id)
        try:
            user_supp_id = message.content.split("$ap register ", 1)[1]
            print(user_supp_id)
            status = add_user(user_id, user_supp_id)
        except IndexError:
            print("no support_id provided")
            status = add_user(user_id, "0")
        await message.channel.send(status)

    elif message.content.startswith("$ap_add_user"):
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            try:
                # user_supp_id = message.content.split("$ap_add_user ", 1)[1]
                temp_str = message.content.split("$ap_add_user ", 1)[1]
                add_user_id = int(temp_str.split()[0])
                # print(lookup_user)
                add_user_supp_id = int(temp_str.split()[1])
                print(add_user_supp_id)
                status = add_user(add_user_id, add_user_supp_id)
            except IndexError:
                print("no support_id provided")
                status = add_user(user_id, "0")
        else:
            output = "You are not authorized to do that."
        await message.channel.send(status)

    elif message.content == "$ap help":
        output = """
```prolog
Command List:
"$ap register" - register new user (self) without supportID
"$ap register [SupportID Number]" - register new user (self) or update an existing user (self) with supportID
"$ap rewards" - list all available rewards (and reward claiming codes)
"$ap check" - check own AP
"$ap claim [reward code]" - claim the reward of your choice using the reward code
"$ap transactions" - view your current pending transaction(s)
"$ap refund [Transaction ID]" - refund your pending transaction
"$ap about" - about AP bot and credits
"$ap help" - this text you see
"$ap riddle" - ???

Command List (Admin Only):
"$ap all transactions" - view all current pending transactions
"$ap close transaction [Transaction ID]" - close a pending transaction, finalize the reward process, can not be refunded with "$ap refund" any more, pending transaction gets removed
"$ap list all users" or "$ap lau" - show all registered users
"$ap aword user [UserID] [AP Amount]" - add specific AP amount to user
```
        """
        await message.channel.send(output)

    elif message.content == "$ap about":
        embed = discord.Embed()
        embed.title = "About Auction Points (AP) bot"
        embed.color = 0x253473
        embed.add_field(name="Version", value="0.9.91", inline=True)
        embed.add_field(name="made by", value="<@353973336654479361>", inline=True)
        embed.add_field(name="hosted on", value="[replit](https://replit.com)", inline=True)
        embed.add_field(name="based on",
                        value="[this tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)",
                        inline=True)
        embed.add_field(name="Alpha tester(s)", value="<@252535294866358273>", inline=True)
        embed.add_field(name="Beta tester(s)", value="<@301361809766744077>\n<@324922454629810204>", inline=True)
        latest_changes = "- added something ???, could be fun :)"
        embed.add_field(name="Latest change", value=latest_changes, inline=False)
        # await ctx.send(embed=embed)
        await message.channel.send(embed=embed)

    elif message.content == "$ap changelog":
        embed = discord.Embed()
        embed.title = "Change log"
        changes = "- better formatting\n- claiming prizes no longer possible without a valid support ID registered\n- certain error messages are now more polite\n- removed underscores for commands\n- no longer always responds to vw bot"
        change_097 = "- nicer embeded about page"
        change_098 = "- added changelog (this)\n- added new rewards to reward list\n- added a warning when user has more than allowed AP (currently 50 AP)\n- community managers get notified on reward claim\n- added some easter eggs, you should 'check' it out"
        change_099 = "- `$ap check` is now embeded (makes it look nicer)\n- minor easter egg bug fix"
        change_0991 = "- something ??? ;)"
        embed.color = 0x253473
        embed.add_field(name="0.9.91", value=change_0991, inline=False)
        embed.add_field(name="0.9.9", value=change_099, inline=False)
        embed.add_field(name="0.9.8", value=change_098, inline=False)
        embed.add_field(name="0.9.7", value=change_097, inline=False)
        embed.add_field(name="0.9.6 and older", value=changes, inline=False)
        await message.channel.send(embed=embed)

    elif message.content == "$ap rewards":
        output = show_rewards()
        await message.channel.send(output)

    elif message.content.startswith("$ap claim"):
        try:
            reward_code = message.content.split("$ap claim ", 1)[1]
        except IndexError:
            reward_code = "0"
        user_id = int(message.author.id)
        current_AP = get_user_AP(user_id)
        current_CT = get_user_CT(user_id)
        supp_id = get_user_supp_ID(user_id)
        output = ""
        if current_AP.isnumeric() == False:
            output = current_AP
        elif reward_code == "0":
            output = "Please provide a valid reward code (example: `$ap claim ABC12`)\nNote: Codes are case sensitive."
        elif str(current_AP) == "0":
            output = "You have 0 AP, you can't afford anything"
        elif str(supp_id) == "0":
            output = "Support ID missing. Please register your support ID, to do that type `$ap register [your support ID]` and try to claim the prize again."
        elif int(current_AP) > 0:
            reward_cost = get_reward_cost(reward_code)
            reward_index = get_reward_index(reward_code)
            current_CT_array = current_CT.split(',')
            if type(reward_cost) == int:
                # print("initiate transaction")
                if (int(current_AP) - int(reward_cost)) >= 0:
                    if int(current_CT_array[reward_index]) < int(time.time()-claim_timeout):
                        # print("sufficient AP")
                        output = create_transaction(user_id, reward_cost, reward_code)
                        new_AP = int(current_AP) - int(reward_cost)
                        current_CT_array[reward_index] = str(int(time.time()))
                        new_CT = ','.join(map(str, current_CT_array))
                        print(new_CT)
                        res = set_user_AP(user_id, new_AP)
                        res2 = set_user_CT(user_id, new_CT)
                        output += "\n```css\nCongratulations " + message.author.name + ",\nyou have claimed the reward [" + get_reward_name(
                            reward_code) + "] for " + str(reward_cost) + " AP\nYou now have " + str(
                            new_AP) + " AP remaining.```"
                        output += "\nCommunity manager <@252535294866358273> has been notified"
                    else:
                        claimable = int(current_CT_array[reward_index]) - int(time.time()-claim_timeout)
                        output = "Unable to claim reward - recently claimed (next claim available in " + str(float(int(claimable/8640)/10)) + " days)."
                else:
                    output = "```Unable to claim reward - insufficient AP```"
            else:
                output = reward_cost
        else:
            output = current_AP
        await message.channel.send(output)

    elif message.content == "$ap riddle":
        is_embed = False
        lookup_user = str(message.author.name)
        lookup_user_id = int(message.author.id)
        output_msg = 'unknown error'
        starts_in = db["riddle_starts_in"]
        current_time = int(time.time())
        if starts_in > current_time:
            output_msg = "Please stand by, next riddle coming up in " + str(
                float(math.floor((starts_in - current_time) / 6) / 10)) + " minutes."
        elif "user_IDs" in db.keys():
            user_list = db["user_IDs"]
            user_APs = db["user_APs"]
            attempts = str(db["riddle_attempts"])
            try:
                lookup_index = user_list.index(lookup_user_id)
                output_msg = CF.riddle_read()
                bounty = db["riddle_points"]
                riddle_author = CF.riddle_author()
                riddle_category = CF.riddle_category()
                if attempts == "0":
                    output_name = "???  (Out of attempts)"
                    output_footer = "To send an answer, type `$ap answer [your answer]`, but the riddle has been been failed."
                    output_reward = "~~" + str(bounty) + " AP~~ (No more attempts remaining)"
                elif CF.riddle_status() == "1":
                    output_name = "???"
                    output_footer = "To send an answer, type `$ap answer [your answer]`"
                    output_reward = str(bounty) + " AP"
                else:
                    output_name = "???  (Already solved)"
                    output_footer = "To send an answer, type `$ap answer [your answer]`, but the riddle has been already solved and the prize was claimed."
                    output_reward = "~~" + str(bounty) + " AP~~ (Claimed)"
                embed = discord.Embed()
                embed.color = 0x253473
                embed.title = output_name
                embed.description = output_msg
                embed.add_field(name="Reward:", value=output_reward, inline=True)
                embed.add_field(name="Remaining attempts:", value=attempts, inline=True)
                embed.add_field(name="Riddle by:", value=riddle_author, inline=True)
                embed.add_field(name="Category:", value=riddle_category, inline=True)
                embed.set_footer(text=output_footer)
                is_embed = True
            except ValueError:
                output_msg = "You are not registered, just type `$ap register` to register."
        if is_embed == True:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(output_msg)

    elif message.content.startswith("$ap answer"):
        is_embed = False
        lookup_user = str(message.author.name)
        lookup_user_id = int(message.author.id)
        user_id = int(message.author.id)
        current_AP = get_user_AP(user_id)
        output_msg = 'unknown error'
        attempts = db["riddle_attempts"]
        starts_in = db["riddle_starts_in"]
        current_time = int(time.time())
        try:
            answer = message.content.split("$ap answer ", 1)[1]
        except IndexError:
            answer = "0"
        if starts_in > current_time:
            output_msg = "Please stand by, next riddle coming up in " + str(
                float(math.floor((starts_in - current_time) / 6) / 10)) + " minutes."
        elif answer == "0":
            output_msg = "Please provide a valid answer for the riddle (example: `$ap answer kittens`)"
        elif answer == "kittens":
            output_msg = "That was just an example... but kittens are cute :3"
        elif current_AP.isnumeric() == False:
            output_msg = "You are not registered, just type `$ap register` to register."
        elif attempts == 0:
            output_msg = "Sorry, you have no more attempts remaining :("
        elif CF.riddle_check(answer) == "0" and CF.riddle_status() == "1":
            attempts -= 1
            db["riddle_attempts"] = attempts
            random_int = str(random.randint(0, 100))
            output_msg = CF.wrong_flavor(random_int)
            if output_msg == "0":
                output_msg = "Sorry, that's not the correct answer.\n" + str(attempts) + " attempt(s) remaining."
            else:
                output_msg += "\n" + str(attempts) + " attempt(s) remaining."
        elif CF.riddle_check(answer) == "0" and CF.riddle_status() == "0":
            output_msg = "Sorry, that's not the correct answer and the riddle has already been solved."
        elif CF.riddle_check(answer) == "1" and CF.riddle_status() == "1":
            if "user_IDs" in db.keys():
                user_list = db["user_IDs"]
                user_APs = db["user_APs"]
                try:
                    lookup_index = user_list.index(lookup_user_id)
                    current_AP = user_APs[lookup_index]
                    add_AP = CF.riddle_trigger()
                    new_total_AP = int(current_AP) + int(add_AP)
                    user_APs[lookup_index] = str(new_total_AP)
                    db["user_APs"] = user_APs
                    output_msg = "Good work <@" + str(
                        user_list[lookup_index]) + ">, you solved the riddle!\nAlso, you win " + str(
                        add_AP) + " AP.\nNow you have " + str(new_total_AP) + " AP."
                    embed = discord.Embed()
                    embed.color = 0x253473
                    embed.add_field(name="Riddle solved!", value=output_msg, inline=False)
                    is_embed = True
                except ValueError:
                    output_msg = "You are not registered, just type `$ap register` to register."
        elif CF.riddle_check(answer) == "1" and CF.riddle_status() == "0":
            output_msg = "Well, you got the answer right, but the reward has already been claimed, better luck next time."
        if is_embed == True:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(output_msg)

    elif message.content.startswith("$ap rearm riddle"):
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            try:
                temp_str = message.content.split("$ap rearm riddle ", 1)[1]
                amount = int(temp_str.split()[0])
                attempts = int(temp_str.split()[1])
                current_time = int(time.time())
                starts_in = (int(temp_str.split()[2]) * 60) + current_time
            except IndexError:
                amount = 1
                attempts = 100
                starts_in = 0
            except ValueError:
                amount = 1
                attempts = 100
                starts_in = 0
            if str(amount).isnumeric() and amount > 0 and amount <= 15:
                db["riddle_trigger"] = "armed"
                db["riddle_points"] = amount
                db["riddle_attempts"] = attempts
                db["riddle_starts_in"] = starts_in
                output = "Riddle rearmed and reward set to " + str(amount) + " AP, " + str(
                    attempts) + " attempts and starts in " + str(int((starts_in - current_time) / 60)) + " minutes."
            else:
                output = "Points out of range (min 1, max 15) or not a number."
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content == ("$ap disarm riddle"):
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            db["riddle_trigger"] = "disarmed"
            db["riddle_starts_in"] = int(time.time())
            output = "Riddle disarmed."
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content == "$ap transactions":
        user_id = int(message.author.id)
        output = show_user_transactions(user_id)
        await message.channel.send(output)

    elif message.content == "$ap all transactions" or message.content == "$ap lat":
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            output = show_all_transactions()
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap close transaction"):
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            try:
                trans_code = message.content.split("$ap close transaction ", 1)[1]
                output = close_transaction(trans_code)
            except IndexError:
                output = close_transaction("0")
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap refund"):
        user_id = int(message.author.id)
        try:
            transaction_code = message.content.split("$ap refund ", 1)[1]
            output = refund_transaction(user_id, transaction_code)
        except IndexError:
            output = refund_transaction(user_id, "0")
        await message.channel.send(output)

    elif message.content == "$ap_clear_trans_db":
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            output_msg = 'transaction DB deleted'
            del db["trans_timestamp"]
            del db["trans_user_id"]
            del db["trans_ap_cost"]
            del db["trans_reward_code"]
        await message.channel.send(output_msg)

    elif message.content == "$ap reset claim timestamps" or message.content == "$ap rct":
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            timestamps = []
            user_list = db["user_IDs"]
            user_num = len(user_list)
            user_current = 0
            while user_current < user_num:
                timestamps.append("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                user_current += 1
            output_msg = "All users claim timestamps reset."
            db["user_CTs"] = timestamps
        await message.channel.send(output_msg)

    elif message.content.startswith("$ap_remove_user"):
        # protected
        user_id = int(message.author.id)
        if is_admin(user_id):
            try:
                lookup_remove_user = message.content.split("$ap_remove_user ", 1)[1]
                if "user_IDs" in db.keys():
                    user_list = db["user_IDs"]
                    if str(lookup_remove_user) in str(user_list):
                        try:
                            lookup_index = user_list.index(int(lookup_remove_user))
                        except ValueError:
                            # lookup_index = 0
                            print("lookup error")
                        user_APs = db["user_APs"]
                        user_supp_ID = db["user_supp_ID"]
                        removed_user = user_list.pop(lookup_index)
                        removed_APs = user_APs.pop(lookup_index)
                        removed_user_supp_ID = user_supp_ID.pop(lookup_index)
                        db["user_IDs"] = user_list
                        db["user_APs"] = user_APs
                        db["user_supp_ID"] = user_supp_ID
                        output = "Removed user '" + str(removed_user) + "' that had " + str(
                            removed_APs) + " AP with Support ID: " + str(removed_user_supp_ID) + "."
                    else:
                        output = "Error - user `" + lookup_remove_user + "` not found."
            except IndexError:
                output = "Error - missing argument [user]"
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap_"):
        await message.channel.send(
            "Unknown command - please type `$ap help` for list of commands. Also, commands don't use underscore any longer.")

    elif message.content.startswith("$ap"):
        user_id = int(message.author.id)
        await message.channel.send("Unknown command - please type `$ap help` for list of commands.")


keep_alive()
client.run(os.environ['TOKEN'])
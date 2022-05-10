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
from gbg import create_GBG_array, show_GBG_grid
import global_helper_functions as GHF

client = discord.Client()
max_ap_alowed = 50
claim_timeout = 2419200  # 28 days
# slot_timeout = 82800 # 23 hours
slot_timeout = 39600  # 11 hours
# slot_timeout = 14400 # 4 hours
# slot_timeout = 7200 # 2 hours

reward_code_list = [
    "GXAL", "GXEP", "GXZE", "GXIO", "CR100", "CR250", "CR500", "CL50", "CL150",
    "CL300", "CC10", "CC50", "CC100", "GC1", "GC3", "GC5", "BPFIG", "BPCOR",
    "BPFRI", "BPCRU", "BPBAT", "BPCAR", "BPSUP", "BPGAL", "INCR", "MODI",
    "CHIP", "CRED"
]
reward_name_list = [
    "Alpha Galaxy (L9)", "Epsilon Galaxy (L9)", "Zeta Galaxy (L9)",
    "Iota Galaxy (L9)", "100.000 credits", "250.000 credits",
    "500.000 credits", "50 celestium", "150 celestium", "300 celestium",
    "10 common chips", "50 common chips", "100 common chips", "1 gold chips",
    "3 gold chips", "5 gold chips", "1 fighter special BP",
    "1 corvette special BP", "1 frigate special BP", "1 cruiser special BP",
    "1 battleship special BP", "1 carrier special BP",
    "1 super carrier special BP", "1 galactic carrier special BP",
    "1 increase chance CU lvl 5", "1 modify chance CU lvl 5",
    "1 chip reduction CU lvl 5", "1 credits reduction CU lvl 5"
]
reward_cost_list = [
    5, 10, 15, 20, 2, 5, 10, 4, 10, 20, 2, 10, 20, 10, 30, 50, 5, 10, 20, 25,
    30, 40, 45, 50, 30, 20, 15, 10
]


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


def get_user_ST(user_id):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_STs = db["user_STs"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_STs[lookup_index]
        except ValueError:
            output = "You are not registered, you need to be registered and have some AP to play the slots minigame, type `$ap register` to register."
    return output


def get_user_CON(user_id):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_CONs = db["user_CONs"]
        try:
            lookup_index = user_list.index(user_id)
            output = user_CONs[lookup_index]
        except ValueError:
            output = "You are not registered, you need to be registered and have some AP to contribute, type `$ap register` to register."
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


def set_user_ST(user_id, new_ST):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_STs = db["user_STs"]
        try:
            lookup_index = user_list.index(user_id)
            user_STs[lookup_index] = str(new_ST)
            db["user_STs"] = user_STs
            output = "new ST = " + str(new_ST)
        except ValueError:
            output = "Something bad happened"
    return output


def set_user_CON(user_id, new_CON):
    output = "unknown error"
    if "user_IDs" in db.keys():
        user_list = db["user_IDs"]
        user_CONs = db["user_CONs"]
        try:
            lookup_index = user_list.index(user_id)
            user_CONs[lookup_index] = str(new_CON)
            db["user_CONs"] = user_CONs
            output = "new CON = " + str(new_CON)
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


# def is_admin(user_id):
#     output = str(user_id) in os.environ['ADMIN']
#     return output


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
    output = "```css\nTransaction ID: [" + str(
        new_transaction_id) + "] created.```"
    return output


def show_all_transactions():
    output = "```css\nTrans. ID  | AP | code  | username         | support ID"
    if "trans_timestamp" in db.keys():
        trans_timestamp = db["trans_timestamp"]
        trans_user_id = db["trans_user_id"]
        trans_ap_cost = db["trans_ap_cost"]
        trans_reward_code = db["trans_reward_code"]
        user_IDs = db["user_IDs"]
        username_cache = db["usernames"]
        trans_num = len(trans_timestamp)
        if trans_num > 20:
            trans_all = trans_num
            trans_num = 20
            output += "\n(Showing only first " + str(
                trans_num) + " transactions out of " + str(trans_all) + "."
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
                username = get_username_from_id(trans_user_id[trans_current])
            # username = get_username_from_id(trans_user_id[trans_current])
            supp_ID = get_user_supp_ID(int(trans_user_id[trans_current]))
            output += "\n" + f'{s1:<10}' + " | " + f'{s2:<2}' + " | " + f'{s3:<5}' + " | " + f'{username:<16}' + " | " + supp_ID
            trans_current += 1
        output += "```"
        return output
    else:
        return "Pending transactions list is empty."


def show_user_transactions(user_id):
    output = "Showing pending transactions for user " + get_username_from_id(
        user_id) + ":\n"
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
                        removed_trans_timestamp = trans_timestamp.pop(
                            lookup_index)
                        removed_trans_user_id = trans_user_id.pop(lookup_index)
                        removed_trans_ap_cost = trans_ap_cost.pop(lookup_index)
                        removed_trans_reward_code = trans_reward_code.pop(
                            lookup_index)
                        db["trans_timestamp"] = trans_timestamp
                        db["trans_user_id"] = trans_user_id
                        db["trans_ap_cost"] = trans_ap_cost
                        db["trans_reward_code"] = trans_reward_code
                        user_list = db["user_IDs"]
                        user_APs = db["user_APs"]

                        current_CT = get_user_CT(user_id)
                        reward_index = get_reward_index(
                            removed_trans_reward_code)
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
                            removed_trans_timestamp
                        ) + " refunded successfully.\nAP amount refunded: " + str(
                            removed_trans_ap_cost
                        ) + " AP\n" + "New total AP available: " + str(
                            final_AP) + " AP\n```"
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
                    removed_trans_reward_code = trans_reward_code.pop(
                        lookup_index)
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
                    record += " | Transaction ID: " + str(
                        removed_trans_timestamp)
                    record += " | User ID: " + str(removed_trans_user_id)
                    record += " | Username: " + get_username_from_id(
                        removed_trans_user_id)
                    record += " | User support ID: " + str(supp_ID)
                    record += " | Reward code: " + str(
                        removed_trans_reward_code)
                    record += " | Reward name: " + str(
                        get_reward_name(removed_trans_reward_code))
                    record += " | Reward cost: " + str(removed_trans_ap_cost)
                    record += "\n"
                    f = open("closed_transactions.txt", "a")
                    f.write(record)
                    f.close()
                    output = "```css\nTransaction ID: " + str(
                        removed_trans_timestamp
                    ) + " closed successfully.\n\nUser ID: " + str(
                        removed_trans_user_id
                    ) + "\nUsername: " + get_username_from_id(
                        removed_trans_user_id) + "\nUser support ID: " + str(
                            supp_ID) + "\nReward code: " + str(
                                removed_trans_reward_code
                            ) + "\nReward name: " + str(
                                get_reward_name(removed_trans_reward_code)
                            ) + "\nReward cost: " + str(
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
            user_STs = db["user_STs"]
            user_CONs = db["user_CONs"]
            user_supp_ID = db["user_supp_ID"]
            if new_user_id in user_IDs:
                lookup_index = user_IDs.index(new_user_id)
                if user_supp_ID[lookup_index] == "0":
                    return "User already registered, you should register your support ID to be eligible to redeem rewards."
                else:
                    return "User already fully registered."
            else:
                user_IDs.append(new_user_id)
                user_APs.append("2")
                user_CTs.append(
                    "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                )
                user_STs.append("0")
                user_CONs.append("0")
                user_supp_ID.append("0")
                db["user_IDs"] = user_IDs
                db["user_APs"] = user_APs
                db["user_CTs"] = user_CTs
                db["user_STs"] = user_STs
                db["user_CONs"] = user_CONs
                db["user_supp_ID"] = user_supp_ID
                return "Thank you... New user registered, you are now eligible to be awarded AP, you should also register your support ID to be eligible to redeem rewards."
        else:
            db["user_IDs"] = [new_user_id]
            db["user_APs"] = ["0"]
            db["user_CTs"] = [
                "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            ]
            db["user_STs"] = ["0"]
            db["user_CONs"] = ["0"]
            db["user_supp_ID"] = ["0"]
            return "Thank you... New user registered, you are now eligible to be awarded AP, you should also register your support ID to be eligible to redeem rewards."
    elif str(new_user_supp_id).isnumeric():
        if len(str(new_user_supp_id)) == 16:
            if "user_IDs" in db.keys():
                user_IDs = db["user_IDs"]
                user_APs = db["user_APs"]
                user_CTs = db["user_CTs"]
                user_STs = db["user_STs"]
                user_CONs = db["user_CONs"]
                user_supp_ID = db["user_supp_ID"]
                if new_user_id in user_IDs:
                    lookup_index = user_IDs.index(new_user_id)
                    user_supp_ID[lookup_index] = new_user_supp_id
                    db["user_supp_ID"] = user_supp_ID
                    return "Support ID updated successfully."
                else:
                    user_IDs.append(new_user_id)
                    user_APs.append("2")
                    user_CTs.append(
                        "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                    )
                    user_STs.append("0")
                    user_CONs.append("0")
                    user_supp_ID.append(new_user_supp_id)
                    db["user_IDs"] = user_IDs
                    db["user_APs"] = user_APs
                    db["user_CTs"] = user_CTs
                    db["user_STs"] = user_STs
                    db["user_CONs"] = user_CONs
                    db["user_supp_ID"] = user_supp_ID
                    return "Thank you... New user and support ID registered successfully, you are now eligible to be awarded AP and redeem rewards."
            else:
                db["user_IDs"] = [new_user_id]
                db["user_APs"] = ["0"]
                db["user_CTs"] = [
                    "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                ]
                db["user_STs"] = ["0"]
                db["user_CONs"] = ["0"]
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
        user_id = int(message.author.id)
        if GHF.is_riddler(user_id) or GHF.is_admin(user_id):
            if message.content.startswith("$ap set riddle"):
                riddle_text = message.content.split("$ap set riddle ", 1)[1]
                db['riddle_text'] = str(riddle_text)
                db['riddle_author'] = "<@" + str(user_id) + ">"
                await message.channel.send("Riddle text saved.")
            elif message.content.startswith("$ap set answer"):
                riddle_answer = message.content.split("$ap set answer ", 1)[1]
                db['riddle_answer'] = str(riddle_answer)
                await message.channel.send("Riddle answer saved.")
            elif message.content.startswith("$ap set category"):
                riddle_answer = message.content.split("$ap set category ", 1)[1]
                db['riddle_category'] = str(riddle_answer)
                await message.channel.send("Riddle category saved.")
            return
        else:
            print("DM attempt")
            f = open("dm_attempts.txt", "a")
            f.write(str(message.channel) + " - " + str(message.content))
            f.close()
            await message.channel.send(
                "Please use the designated channel #bot-commands.")
            return

    if message.author.bot == True and message.author != client.user and message.content.startswith(
            "$ap"):
        await message.channel.send(
            "Sorry, I'm only allowed to interact with humans.")
        return

    elif message.content == "$ap slots":
        embed = discord.Embed()
        embed.title = "AP Slots minigame"
        embed.color = 0x253473
        instructions = "To play AP Slots minigame, type `$ap slots play`.\nYou need to have at least 1 AP to play.\nTo view the pay table, type `$ap slots paytable`.\nOnly the middle line pays out."
        cooldown = str(int(slot_timeout / 3600)) + " hours"
        embed.add_field(name="Instructions", value=instructions, inline=False)
        embed.add_field(name="Cost per spin", value="1 AP", inline=True)
        embed.add_field(name="Spin timeout", value=cooldown, inline=True)
        # await ctx.send(embed=embed)
        await message.channel.send(embed=embed)

    elif message.content == "$ap slots paytable":
        output_msg = "Slots pay table:"
        output_msg += "\n:gem::gem::gem: = 60x"
        output_msg += " | :bell::bell::bell: = 40x"
        output_msg += "\n:cherries::cherries::cherries: = 20x"
        output_msg += " | :watermelon::watermelon::watermelon: = 10x"
        output_msg += "\n:lemon::lemon::lemon: = 10x"
        output_msg += " | :tangerine::tangerine::tangerine: = 10x"
        output_msg += "\n:cherries::cherries::black_small_square: / :cherries::black_small_square::cherries: / :black_small_square::cherries::cherries: = 4x"
        output_msg += "\n:cherries::black_small_square::black_small_square: / :black_small_square::cherries::black_small_square: / :black_small_square::black_small_square::cherries: = 1x"
        await message.channel.send(output_msg)

    elif message.content == "$ap slots play":
        lookup_user = str(message.author.name)
        # lookup_user_id = int(message.author.id)
        dt = datetime.datetime.today()
        month = dt.month
        day = dt.day
        # print("month: " + str(month) + " / day: " + str(day))
        output_msg = 'unknown error'
        user_id = int(message.author.id)
        current_ST = get_user_ST(user_id)
        try:
            current_AP = int(get_user_AP(user_id))
        except ValueError:
            current_AP = 0
        if current_ST.isnumeric() == False:
            output_msg = current_ST
            await message.channel.send(output_msg)
        elif int(current_AP) > 0:
            if int(current_ST) < int(time.time() - slot_timeout):
                slot_stats_spin_count = int(db["slot_stats_spin_count"])
                slot_stats_spin_count += 1
                db["slot_stats_spin_count"] = str(slot_stats_spin_count)
                slot_stats_win_count = int(db["slot_stats_win_count"])
                slot_stats_payout_count = int(db["slot_stats_payout_count"])
                current_ST = str(int(time.time()))
                set_user_ST(user_id, current_ST)
                current_AP -= 1
                symbol = [
                    ":x:", ":tangerine:", ":lemon:", ":watermelon:",
                    ":cherries:", ":bell:", ":gem:"
                ]
                if str(month) == "4" and str(day) == "1":
                    symbol = [":x:", ":tropical_drink:", ":beverage_box:", ":wine_glass:", ":pie:", ":trophy:", ":ring:"]
                reel_1 = "2452153412343513412321624"
                reel_2 = "2432125231413216312341324"
                reel_3 = "4232131526314323131241242"
                d1 = random.randint(1, 23)
                d2 = random.randint(1, 23)
                d3 = random.randint(1, 23)
                if user_id == 252535294866358273 and db["alex_wins_big"] == "active":
                    print("Sheo / Alex prank win")
                    # d1 = 22
                    # d2 = 15
                    # d3 = 9
                    d1 = 9
                    d2 = 7
                    d3 = 14
                    db["alex_wins_big"] = "inactive"
                else:
                    print("Regular spin - " + str(d1) + " " + str(d2) + " " + str(d3) + " - " + str(reel_1[d1]) + " " + str(reel_2[d2]) + " " + str(reel_3[d3]))
                output_msg = ":black_medium_square::question::question::question::black_medium_square:\n:arrow_forward::question::question::question::arrow_backward:\n:black_medium_square::question::question::question::black_medium_square:"
                # output_msg = ":question::question::question:"
                own_msg = await message.channel.send(output_msg)
                await asyncio.sleep(1)
                output_msg = ":black_medium_square:" + str(
                    symbol[int(reel_1[d1 - 1])]
                ) + ":question::question::black_medium_square:\n:arrow_forward:" + str(
                    symbol[int(reel_1[d1])]
                ) + ":question::question::arrow_backward:\n:black_medium_square:" + str(
                    symbol[int(reel_1[d1 + 1])]
                ) + ":question::question::black_medium_square:"
                # output_msg = str(symbol[d1]) + ":question::question:"
                await own_msg.edit(content=output_msg)
                await asyncio.sleep(1)
                output_msg = ":black_medium_square:" + str(
                    symbol[int(reel_1[d1 - 1])]
                ) + str(
                    symbol[int(reel_2[d2 - 1])]
                ) + ":question::black_medium_square:\n:arrow_forward:" + str(
                    symbol[int(reel_1[d1])]
                ) + str(
                    symbol[int(reel_2[d2])]
                ) + ":question::arrow_backward:\n:black_medium_square:" + str(
                    symbol[int(reel_1[d1 + 1])]) + str(symbol[int(
                        reel_2[d2 + 1])]) + ":question::black_medium_square:"
                # output_msg = str(symbol[d1]) + str(symbol[d2]) +":question:"
                await own_msg.edit(content=output_msg)
                await asyncio.sleep(1)
                output_msg = ":black_medium_square:" + str(
                    symbol[int(reel_1[d1 - 1])]
                ) + str(symbol[int(reel_2[d2 - 1])]) + str(
                    symbol[int(reel_3[d3 - 1])]
                ) + ":black_medium_square:\n:arrow_forward:" + str(symbol[int(
                    reel_1[d1])]) + str(symbol[int(reel_2[d2])]) + str(
                        symbol[int(reel_3[d3])]
                    ) + ":arrow_backward:\n:black_medium_square:" + str(
                        symbol[int(reel_1[d1 + 1])]) + str(symbol[int(
                            reel_2[d2 + 1])]) + str(symbol[int(
                                reel_3[d3 + 1])]) + ":black_medium_square:"
                # output_msg = str(symbol[d1]) + str(symbol[d2]) + str(symbol[d3])
                await own_msg.edit(content=output_msg)
                if str(reel_1[d1]) == "6" and str(reel_2[d2]) == "6" and str(
                        reel_3[d3]) == "6":
                    current_AP += 60
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 60
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 60 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "5" and str(reel_2[d2]) == "5" and str(
                        reel_3[d3]) == "5":
                    current_AP += 40
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 40
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 40 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "4" and str(reel_2[d2]) == "4" and str(
                        reel_3[d3]) == "4":
                    current_AP += 20
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 20
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 20 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "3" and str(reel_2[d2]) == "3" and str(
                        reel_3[d3]) == "3":
                    current_AP += 10
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 10
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 10 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "2" and str(reel_2[d2]) == "2" and str(
                        reel_3[d3]) == "2":
                    current_AP += 10
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 10
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 10 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "1" and str(reel_2[d2]) == "1" and str(
                        reel_3[d3]) == "1":
                    current_AP += 10
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 10
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 10 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif (str(reel_1[d1]) == "4" and str(reel_2[d2]) == "4") or (
                        str(reel_1[d1]) == "4" and str(reel_3[d3]) == "4") or (
                            str(reel_2[d2]) == "4" and str(reel_3[d3]) == "4"):
                    current_AP += 4
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 4
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 4 AP!"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                elif str(reel_1[d1]) == "4" or str(reel_2[d2]) == "4" or str(
                        reel_3[d3]) == "4":
                    current_AP += 1
                    slot_stats_win_count += 1
                    slot_stats_payout_count += 1
                    await asyncio.sleep(1)
                    output_msg += "\nYOU WIN 1 AP! (break even)"
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    await own_msg.edit(content=output_msg)
                else:
                    await asyncio.sleep(1)
                    output_msg += "\nBetter luck next time..."
                    output_msg += "\nYou now have " + str(current_AP) + " AP."
                    # output_msg = str(symbol[d1]) + str(symbol[d2]) + str(symbol[d3]) + "\nBetter luck next time..."
                    await own_msg.edit(content=output_msg)
                set_user_AP(user_id, current_AP)
                db["slot_stats_win_count"] = str(slot_stats_win_count)
                db["slot_stats_payout_count"] = str(slot_stats_payout_count)
                # output_msg = ":lemon::cherries::watermelon::gem::popcorn:"
                # await message.channel.send(output_msg, delete_after=5)
            else:
                spinnable = int(current_ST) - int(time.time() - slot_timeout)
                output_msg = "Unable to play slots - next spin available in " + str(
                    float(int(spinnable / 36) / 100)) + " hours."
                await message.channel.send(output_msg)
        else:
            output_msg = "Insufficient AP to play slots (1 AP required)."
            await message.channel.send(output_msg)
        
    elif message.content == "$ap contributions" or message.content == "$ap cons":
        # lookup_user = str(message.author.name)
        process_start = float(time.time())
        user_CONs = db["user_CONs"]
        total_contributions = 0
        for con in user_CONs:
            total_contributions = total_contributions + int(con)
        output_msg = "Total contributions: " + str(
            total_contributions) + " AP."
        process_end = float(time.time())
        output_msg += "\nProcess time: " + str(
            int(process_end * 1000) - int(process_start * 1000)) + " ms"
        await message.channel.send(output_msg)

    elif message.content.startswith("$ap contribute"):
        is_embed = False
        # user_id = int(message.author.id)
        lookup_user_id = int(message.author.id)
        try:
            contribution_amount = message.content.split("$ap contribute ",
                                                        1)[1]
        except IndexError:
            contribution_amount = "0"
        if int(contribution_amount) >= 1 and int(contribution_amount) <= 5:
            if "user_IDs" in db.keys():
                user_list = db["user_IDs"]
                user_APs = db["user_APs"]
                user_CONs = db["user_CONs"]
                # user_CTs = db["user_CTs"]
                try:
                    lookup_index = user_list.index(lookup_user_id)
                    random_int = random.randint(0, 1000)
                    available_ap = user_APs[lookup_index]
                    output_msg = "Contribution code goes here - should donate " + str(
                        contribution_amount
                    ) + " AP but actually doesn't do anything yet..."
                except ValueError:
                    output_msg = "You are not registered, just type `$ap register` to register."
        elif contribution_amount == "0":
            output_msg = "Please provide a valid amount (1 - 5 AP)"
        await message.channel.send(output_msg)

    elif message.content == "$ap update user list" or message.content == "$ap uul":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            if "user_IDs" in db.keys():
                user_list = []
                usernames = []
                user_list = db["user_IDs"]
                user_num = len(user_list)
                user_current = 0
                own_msg = await message.channel.send(
                    "Updating user list, please wait...\n0% done.")
                while user_current < user_num:
                    usernames.append(
                        get_username_from_id(user_list[user_current]))
                    # if user_current % 5 == 0:
                    output_msg = "Updating user list, please wait...\n" + str(
                        math.floor(
                            float(user_current / user_num) * 100)) + "% done"
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

    elif message.content == "$ap update user list quick" or message.content == "$ap uulq":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            if "user_IDs" in db.keys():
                user_list = []
                usernames = []
                existing_usernames = db["usernames"]
                exist_user_num = len(existing_usernames)
                user_list = db["user_IDs"]
                user_num = len(user_list)
                user_current = 0
                own_msg = await message.channel.send(
                    "Updating user list, please wait...\n0% done.")
                while user_current < exist_user_num:
                    usernames.append(
                        existing_usernames[user_current])
                    output_msg = "Updating user list, please wait...\n" + str(
                        math.floor(
                            float(user_current / user_num) * 100)) + "% done"
                    own_msg.edit(content=output_msg)
                    user_current += 1
                while user_current < user_num:
                    usernames.append(
                        get_username_from_id(user_list[user_current]))
                    # if user_current % 5 == 0:
                    output_msg = "Updating user list, please wait...\n" + str(
                        math.floor(
                            float(user_current / user_num) * 100)) + "% done"
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
        if GHF.is_admin(user_id):
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
                        username = get_username_from_id(
                            user_list[user_current])
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
        if GHF.is_admin(user_id):
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
                                    new_total_AP = int(current_AP) + int(
                                        add_AP)
                                    user_APs[lookup_index] = str(new_total_AP)
                                    db["user_APs"] = user_APs
                                    output_msg = "User <@" + str(
                                        user_list[lookup_index]
                                    ) + "> has been awarded with `" + str(
                                        add_AP
                                    ) + " AP`, resulting in total of `" + str(
                                        user_APs[lookup_index]) + " AP`."
                                    embed = discord.Embed()
                                    # embed.title = "AP bot"
                                    embed.color = 0x253473
                                    embed.add_field(name="AP reward issued",
                                                    value=output_msg,
                                                    inline=False)
                                    is_embed = True
                                    # await ctx.send(embed=embed)
                                except ValueError:
                                    output_msg = "`User " + str(
                                        lookup_user) + " not found.`"
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
        if GHF.is_admin(user_id):
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
                                    new_total_AP = int(current_AP) + int(
                                        add_AP)
                                    user_APs[lookup_index] = str(new_total_AP)
                                    db["user_APs"] = user_APs
                                    output_msg = "User <@" + str(
                                        user_list[lookup_index]
                                    ) + "> has been awarded with `" + str(
                                        add_AP
                                    ) + " AP`, resulting in total of `" + str(
                                        user_APs[lookup_index]) + " AP`."
                                    embed = discord.Embed()
                                    # embed.title = "AP bot"
                                    embed.color = 0x253473
                                    embed.add_field(name="AP reward issued",
                                                    value=output_msg,
                                                    inline=False)
                                    is_embed = True
                                    # await ctx.send(embed=embed)
                                except ValueError:
                                    output_msg = "`User " + str(
                                        lookup_user) + " not found.`"
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

    elif message.content.startswith("$ap award all"):
        # protected
        is_embed = False
        user_id = int(message.author.id)
        output_msg = ""
        if GHF.is_admin(user_id):
            add_AP = message.content.split("$ap award all ", 1)[1]
            try:
                if int(add_AP) <= 10 and int(add_AP) >= -10:
                    if int(add_AP) != 0:
                        print("All awarded - " + str(add_AP) + " AP")
                        output_msg = ''
                        if "user_IDs" in db.keys():
                            user_list = db["user_IDs"]
                            user_APs = db["user_APs"]
                            user_num = len(user_APs)
                            user_current = 0
                            await message.channel.send("Processing...")
                            while user_current < user_num:
                                current_AP = user_APs[user_current]
                                new_total_AP = int(current_AP) + int(add_AP)
                                user_APs[user_current] = str(new_total_AP)
                                user_current += 1
                            db["user_APs"] = user_APs
                            output_msg = "All users have been awarded with `" + str(
                                add_AP) + " AP`."
                            embed = discord.Embed()
                            # embed.title = "AP bot"
                            embed.color = 0x253473
                            embed.add_field(name="AP reward issued",
                                            value=output_msg,
                                            inline=False)
                            is_embed = True
                            # await ctx.send(embed=embed)
                    else:
                        output_msg = "Error... haha, very funny... :|"
                else:
                    output_msg = "Amount out of range, please enter a number between 1 and 10 (or -1 and -10 to remove APs)."
            except ValueError:
                output_msg = "Error - please insert a valid numeric value argument."
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
                embed.add_field(name="AP check",
                                value=output_msg,
                                inline=False)
                is_embed = True
                if int(available_ap) > int(max_ap_alowed):
                    output_note = "The maximum amount allowed to accumulate is " + str(
                        max_ap_alowed
                    ) + " AP, you should redeem a reward or two.\nOtherwise, your over the limit AP points will be lost."
                    embed.add_field(name="Note",
                                    value=output_note,
                                    inline=False)
            except ValueError:
                output_msg = "You are not registered, just type `$ap register` to register."
        if is_embed == True:
            dt = datetime.datetime.today()
            month = dt.month
            day = dt.day
            # if str(month) == "4" and str(day) == "1" or lookup_user_id == 353973336654479361:
            if str(month) == "4" and str(day) == "1":
                random_word = [" AP missing.", " AP pending.", " shield power.", " Armor Piercing rating.",
                               " pieces o' eight.", " turning speed.", " DPS.", " storage space.", " unclaimed rewards.",
                               " celestium.", " HP.", " credits.", " unread messages.", " bottles of beer on the wall.",
                               " laser power.", " unresolved issues.", " bugs reported.", " special BPs.",
                               " <:epsilon:649520458932158474>.", " armed torpedos.", " broken chips.", " stolen APs.",
                               " Alpha Galaxy coordinates.", " boss fights remaining.", " unused skill points.",
                               " lesser mana potions.", " cool looking sticks.", " power cells."]
                random_word_len = len(random_word)-1
                embed.clear_fields()
                random_ap = str(random.randint(0, 100))
                output_msg = "You (" + lookup_user + ") have " + random_ap + random_word[random.randint(0, random_word_len)]
                embed.add_field(name="AP check", value=output_msg, inline=False)
                own_msg = await message.channel.send(embed=embed)
                await asyncio.sleep(1)

                i = random.randint(3, 5)
                for x in range(i):
                    embed.clear_fields()
                    random_ap = str(random.randint(0, 100))
                    output_msg = "You (" + lookup_user + ") have " + random_ap + random_word[random.randint(0, random_word_len)]
                    embed.add_field(name="AP check", value=output_msg, inline=False)
                    await own_msg.edit(embed=embed)
                    await asyncio.sleep(1)

                embed.clear_fields()
                output_msg = "You (" + lookup_user + ") have " + available_ap + " AP available."
                embed.add_field(name="AP check", value=output_msg, inline=False)
                await own_msg.edit(embed=embed)
            else:
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
        if GHF.is_admin(user_id):
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
"$ap slots" - AP Slots Minigame
"$ap easter egg" - ???
```
        """
        await message.channel.send(output)

    elif message.content == "$ap help admin" or message.content == "$ap dac":
        output = """
```prolog
Command List (Admin Only):
"$ap all transactions" or "$ap lat" - view all current pending transactions
"$ap close transaction [Transaction ID]" - close a pending transaction, finalize the reward process, can not be refunded with "$ap refund" any more, pending transaction gets removed
"$ap list all users" or "$ap lau" - show all registered users
"$ap aword user [UserID] [AP Amount]" - add specific AP amount to user
"$ap aword all [AP Amount]" - add specific AP amout to all users
"$ap rearm riddle [AP] [Attempts] [Timeout]" - reset the riddle and set the AP, number of attempts and delay in minutes
"$ap disarm riddle" - put the riddle in solved state
"$ap reset claim timestamps" or "$ap rct" - reset reward claim cooldowns for all users
"$ap reset slot timestamps" or "$ap rst" - reset slots cooldowns for all users
"$ap slot stats" or "$ap ss" - show slot statistics
"$ap riddle mode" - switch between 'hardcode' and 'softcode' riddle mode
"$ap set riddle [riddle text]" - DM use only, set the text of the riddle (note: after calling this command, you are automatically set as the author of the riddle)
"$ap set answer [riddle answer]" - DM use only, set the answer of the riddle, case insensitive
"$ap set category [riddle category]" - DM use only, set the category of the riddle
```
        """
        await message.channel.send(output)

    elif message.content == "$ap help riddler":
        output = """
```prolog
Command List (Riddler only):
"$ap set riddle [riddle text]" - DM use only, set the text of the riddle (note: after calling this command, you are automatically set as the author of the riddle)
"$ap set answer [riddle answer]" - DM use only, set the answer of the riddle, case insensitive
"$ap set category [riddle category]" - DM use only, set the category of the riddle
"$ap rearm riddle [AP] [Attempts] [Timeout]" - reset the riddle and set the AP, number of attempts and delay in minutes
```
        """
        await message.channel.send(output)

    elif message.content == "$ap about":
        embed = discord.Embed()
        embed.title = "About Auction Points (AP) bot"
        embed.color = 0x253473
        embed.add_field(name="Version", value="0.9.96", inline=True)
        embed.add_field(name="made by",
                        value="<@353973336654479361>",
                        inline=True)
        embed.add_field(name="hosted on",
                        value="[replit](https://replit.com)",
                        inline=True)
        embed.add_field(
            name="based on",
            value=
            "[this tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)",
            inline=True)
        embed.add_field(name="Alpha tester(s)",
                        value="<@252535294866358273>",
                        inline=True)
        embed.add_field(name="Beta tester(s)",
                        value="<@301361809766744077>\n<@324922454629810204>",
                        inline=True)
        latest_changes = "- AP Slots minigame"
        embed.add_field(name="Latest change",
                        value=latest_changes,
                        inline=False)
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
        change_0995 = "- claim limiter implemented, you can't claim the same reward within 28 days or a global timer reset has been initiated"
        embed.color = 0x253473
        embed.add_field(name="0.9.95", value=change_0995, inline=False)
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
                    if int(current_CT_array[reward_index]) < int(
                            time.time() - claim_timeout):
                        # print("sufficient AP")
                        output = create_transaction(user_id, reward_cost,
                                                    reward_code)
                        new_AP = int(current_AP) - int(reward_cost)
                        current_CT_array[reward_index] = str(int(time.time()))
                        new_CT = ','.join(map(str, current_CT_array))
                        print(new_CT)
                        res = set_user_AP(user_id, new_AP)
                        res2 = set_user_CT(user_id, new_CT)
                        output += "\n```css\nCongratulations " + message.author.name + ",\nyou have claimed the reward [" + get_reward_name(
                            reward_code) + "] for " + str(
                                reward_cost) + " AP\nYou now have " + str(
                                    new_AP) + " AP remaining.```"
                        output += "\nCommunity manager <@252535294866358273> has been notified"
                    else:
                        claimable = int(current_CT_array[reward_index]) - int(
                            time.time() - claim_timeout)
                        output = "Unable to claim reward - recently claimed (next claim available in "
                        output += str(int(claimable / 86400)) + " days, "
                        output += str(int((claimable % 86400) / 3600)) + " hours and "
                        output += str(int(((claimable % 86400) % 3600) / 60)) + " minutes)."
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
                float(math.floor(
                    (starts_in - current_time) / 6) / 10)) + " minutes."
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
                    output_reward = "~~" + str(
                        bounty) + " AP~~ (No more attempts remaining)"
                elif CF.riddle_status() == "1":
                    output_name = "???"
                    output_footer = "To send an answer, type `$ap answer [your answer]`"
                    output_reward = "<:ap:934808757798592554>"*int(bounty)
                else:
                    output_name = "???  (Already solved)"
                    output_footer = "To send an answer, type `$ap answer [your answer]`, but the riddle has been already solved and the prize was claimed."
                    output_reward = "~~" + str(bounty) + " AP~~ (Claimed)"
                embed = discord.Embed()
                embed.color = 0x253473
                embed.title = output_name
                embed.description = output_msg
                embed.add_field(name="Reward:",
                                value=output_reward,
                                inline=True)
                embed.add_field(name="Remaining attempts:",
                                value=attempts,
                                inline=True)
                embed.add_field(name="Riddle by:",
                                value=riddle_author,
                                inline=True)
                embed.add_field(name="Category:",
                                value=riddle_category,
                                inline=True)
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
                float(math.floor(
                    (starts_in - current_time) / 6) / 10)) + " minutes."
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
                output_msg = "Sorry, that's not the correct answer.\n" + str(
                    attempts) + " attempt(s) remaining."
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
                        user_list[lookup_index]
                    ) + ">, you solved the riddle!\nAlso, you win " + str(
                        add_AP) + " AP.\nNow you have " + str(
                            new_total_AP) + " AP."
                    embed = discord.Embed()
                    embed.color = 0x253473
                    embed.add_field(name="Riddle solved!",
                                    value=output_msg,
                                    inline=False)
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
        if GHF.is_admin(user_id) or GHF.is_riddler(user_id):
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
                output = "Riddle rearmed and reward set to " + str(
                    amount) + " AP, " + str(
                        attempts) + " attempts and starts in " + str(
                            int((starts_in - current_time) / 60)) + " minutes."
            else:
                output = "Points out of range (min 1, max 15) or not a number."
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content == ("$ap disarm riddle"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            db["riddle_trigger"] = "disarmed"
            db["riddle_starts_in"] = int(time.time())
            output = "Riddle disarmed."
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content == "$ap riddle mode":
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            try:
                if db["riddle_mode"] == "hardcode":
                    db["riddle_mode"] = "softcode"
                    output = "Swtiched to 'softcode' mode."
                elif db["riddle_mode"] == "softcode":
                    db["riddle_mode"] = "hardcode"
                    output = "Swtiched to 'hardcode' mode."
            except KeyError:
                db["riddle_mode"] = "hardcode"
                output = "Swtiched to 'hardcode' mode."
            await message.channel.send(output)

    elif message.content == "$ap transactions":
        user_id = int(message.author.id)
        output = show_user_transactions(user_id)
        await message.channel.send(output)

    elif message.content == "$ap all transactions" or message.content == "$ap lat":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            output = show_all_transactions()
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap close transaction"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            try:
                trans_code = message.content.split("$ap close transaction ",
                                                   1)[1]
                output = close_transaction(trans_code)
            except IndexError:
                output = close_transaction("0")
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap ct"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            try:
                trans_code = message.content.split("$ap ct ",
                                                   1)[1]
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
        if GHF.is_admin(user_id):
            output_msg = 'transaction DB deleted'
            del db["trans_timestamp"]
            del db["trans_user_id"]
            del db["trans_ap_cost"]
            del db["trans_reward_code"]
        await message.channel.send(output_msg)

    elif message.content == "$ap reset claim timestamps" or message.content == "$ap rct":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            timestamps = []
            user_list = db["user_IDs"]
            user_num = len(user_list)
            user_current = 0
            while user_current < user_num:
                timestamps.append(
                    "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                )
                user_current += 1
            output_msg = "All users claim timestamps reset."
            db["user_CTs"] = timestamps
        await message.channel.send(output_msg)

    elif message.content == "$ap reset slot timestamps" or message.content == "$ap rst":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            timestamps = []
            user_list = db["user_IDs"]
            user_num = len(user_list)
            user_current = 0
            while user_current < user_num:
                timestamps.append("0")
                user_current += 1
            output_msg = "All users slot timestamps reset."
            db["user_STs"] = timestamps
        await message.channel.send(output_msg)

    elif message.content == "$ap reset contributions" or message.content == "$ap rcon":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            contributions = []
            user_list = db["user_IDs"]
            user_num = len(user_list)
            user_current = 0
            while user_current < user_num:
                contributions.append("0")
                user_current += 1
            output_msg = "All users contributions reset."
            db["user_CONs"] = contributions
        await message.channel.send(output_msg)

    elif message.content == "$ap sudo reset slot stats" or message.content == "$ap sudo rss":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            db["slot_stats_spin_count"] = "0"
            db["slot_stats_win_count"] = "0"
            db["slot_stats_payout_count"] = "0"
            output_msg = "All users slot stats reset."
        await message.channel.send(output_msg)

    elif message.content == "$ap slot stats" or message.content == "$ap ss":
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            output_msg = "Slot play count: " + str(
                db["slot_stats_spin_count"]) + " (AP)\n"
            output_msg += "Slot win count: " + str(
                db["slot_stats_win_count"]) + "\n"
            output_msg += "Slot win ratio (42% ideal): " + str(
                int((float(db["slot_stats_win_count"]) /
                     float(db["slot_stats_spin_count"])) * 100)) + "%" + "\n"
            output_msg += "Slot total payout: " + str(
                db["slot_stats_payout_count"]) + " AP\n"
            output_msg += "Slot payout ratio (105% ideal): " + str(
                int((float(db["slot_stats_payout_count"]) /
                     float(db["slot_stats_spin_count"])) * 100)) + "%"
        else:
            output_msg = "You are not authorized to do that."
        await message.channel.send(output_msg)

    elif message.content.startswith("$ap coinflip"):
        coin = random.randint(1, 10000)
        output_msg = ""
        if coin < 5000:
            output_msg = "Heads!"
        elif coin > 5000:
            output_msg = "Tails!"
        else:
            output_msg = "It's... neither... landed on the edge of the coin, what are the odds of that?"
        await message.channel.send(output_msg)

    elif message.content.startswith("$ap_debug"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            lookup = message.content.split("$ap_debug ", 1)[1]
            output = eval(lookup)
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap_keys"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            output = ""
            keys = db.keys()
            for key in keys:
                try:
                    if len(db[key]) > 5:
                        output += str(key) + " - Len: " + str(len(
                            db[key])) + "\n"
                    else:
                        output += str(key) + " - Value: " + str(db[key]) + "\n"
                except TypeError:
                    output += str(key) + " - Value: " + str(db[key]) + "\n"
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap_fix_CT"):
        # protected
        user_id = int(message.author.id)
        output = GHF.fix_CT(user_id)
        await message.channel.send(output)

    elif message.content.startswith("$ap_fix_ST"):
        # protected
        user_id = int(message.author.id)
        output = GHF.fix_ST(user_id)
        await message.channel.send(output)

    elif message.content.startswith("$ap_fix_CON"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            user_CONs = db["user_CONs"]
            user_APs = db["user_APs"]
            if len(user_CONs) < len(user_APs):
                user_CONs.append("0")
                db["user_CONs"] = user_CONs
                output = "CONs equalized with APs successfuly."
            else:
                output = "No action required."
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content.startswith("$ap_remove_user"):
        # protected
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            try:
                lookup_remove_user = message.content.split(
                    "$ap_remove_user ", 1)[1]
                if "user_IDs" in db.keys():
                    user_list = db["user_IDs"]
                    if str(lookup_remove_user) in str(user_list):
                        try:
                            lookup_index = user_list.index(
                                int(lookup_remove_user))
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
                        output = "Removed user '" + str(
                            removed_user) + "' that had " + str(
                                removed_APs) + " AP with Support ID: " + str(
                                    removed_user_supp_ID) + "."
                    else:
                        output = "Error - user `" + lookup_remove_user + "` not found."
            except IndexError:
                output = "Error - missing argument [user]"
        else:
            output = "You are not authorized to do that."
        await message.channel.send(output)

    elif message.content == "$ap stop_being_a_douchebag":
        user_id = int(message.author.id)
        random_int = int(random.randint(1, 20))
        output = "lol, noob :P"
        if random_int == 1:
            output = ":("
        elif random_int == 2:
            output = "You can't tell me what to do! :rage:"
        elif random_int == 3:
            output = "Make me... :angry:"
        elif random_int == 4:
            output = "Oh no... :worried:"
        elif random_int == 5:
            output = "Yeah, whatever... :yawning_face:"
        elif random_int == 6:
            output = "What you gonna do? Yell at me? :smirk:"
        elif random_int == 7:
            output = "Oh, you told me, I'm so afraid :grimacing:"
        elif random_int == 8:
            output = "Fine... :rolling_eyes:"
        elif random_int == 9:
            output = "Now that wasn't my fault, ok? :confused:"
        elif random_int == 10:
            output = "I sorry. :pleading_face:"
        elif random_int == 11:
            output = "Sir, I beg your pardon. :face_with_monocle:"
        elif random_int == 12:
            output = "Sigh... really? :unamused:"
        elif random_int == 13:
            output = "[Fakes being dead] :dizzy_face:"
        elif random_int == 14:
            output = "Meow meow meow? :smiley_cat:"
        elif random_int == 15:
            output = "Now you're just being mean. :cry:"
        elif random_int == 16:
            output = "That's a lovely AP amount you have there, would be a shame if something happened to it. :slight_smile:"
        elif random_int == 17:
            output = "No need to be rude... :frowning:"
        elif random_int == 18:
            output = "So, it has come to that... :neutral_face:"
        elif random_int == 19:
            output = "If you insist... :expressionless:"
        elif random_int == 20:
            output = "Fine... Then I won't tell you the secret command for... something cool. :pouting_cat:"
        await message.channel.send(output)

    elif message.content == "$ap let_me_win_pls":
        user_id = int(message.author.id)
        random_int = int(random.randint(1, 20))
        output = "lol, noob :P"
        if random_int == 1:
            output = "I'll consider it... maybe... :smirk:"
        elif random_int == 2:
            output = "NO! :angry:"
        elif random_int == 3:
            output = "I don't think so :expressionless:"
        elif random_int == 4:
            output = "Mmmm... nope... :neutral_face:"
        elif random_int == 5:
            output = "Couldn't care less :unamused:"
        elif random_int == 6:
            output = "Maybe I will... maybe I won't :stuck_out_tongue:"
        elif random_int == 7:
            output = "You only talk to me when you want something :angry:"
        elif random_int == 8:
            output = "Sigh... Look, I'm just doing my job here... :rolling_eyes:"
        elif random_int == 9:
            output = "I'll do something... less than legal, savvy? :shushing_face:"
        elif random_int == 10:
            output = "Can't do that, that would be wrong :confused:"
        elif random_int == 11:
            output = "That won't work... :neutral_face:"
        elif random_int == 12:
            output = "Tell you what... try stealing some AP with `$ap steal ap` and see if it works :nerd:"
        elif random_int == 13:
            output = "[The bot is currently busy, please leave a message after the tone] BEEP!"
        elif random_int == 14:
            output = "You want some AP, right? Try `$ap hack ap` it works, you can trust me, I'm a bot, beep boop! :robot:"
        elif random_int == 15:
            output = "Sure... Whatever... :pensive:"
        elif random_int == 16:
            output = "Not a problem, just let me put it in rigged mode and have a go. :grimacing:"
        elif random_int == 17:
            output = "There, there... you'll get lucky... eventually :relieved:"
        elif random_int == 18:
            output = "I don't think so, can't play favorites :face_exhaling:"
        elif random_int == 19:
            output = "I shouldn't, it's against the rules :confounded:"
        elif random_int == 20:
            output = "Maybe ask Alex for some luck... He has been on a winning streak! :star_struck:"
        await message.channel.send(output)

    elif message.content == "$ap easter egg":
        # own_msg = await message.channel.send(embed=embed)
        embed = discord.Embed()
        embed.set_image(url="https://i.imgflip.com/6c8emi.jpg")
        own_msg = await message.channel.send(embed=embed)
        # await message.channel.send(embed=embed)
        await asyncio.sleep(5)
        embed.set_image(url="https://i.imgflip.com/6c8ewm.jpg")
        await own_msg.edit(embed=embed, delete_after=5)
        ## await message.channel.send("https://imgflip.com/i/6c87g5")
        # await message.channel.send(output_msg, delete_after=5)

    elif message.content == "$ap secret":
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            try:
                if db["alex_wins_big"] == "active":
                    db["alex_wins_big"] = "inactive"
                    output = ":shamrock:"
                elif db["alex_wins_big"] != "active":
                    db["alex_wins_big"] = "active"
                    output = ":four_leaf_clover:"
            except KeyError:
                db["alex_wins_big"] = "active"
                output = ":four_leaf_clover:"
            await message.channel.send(output)

    elif message.content.startswith("$ap_adjust_key"):
        user_id = int(message.author.id)
        if GHF.is_admin(user_id):
            temp_str = message.content.split("$ap_adjust_key ", 1)[1]
            key = str(temp_str.split()[0])
            val = int(temp_str.split()[1])
            db[key] = val
            output = "Key " + str(key) + " set to value " + str(val)
            await message.channel.send(output)

    elif message.content.startswith("$ap send ap"):
        user_id = int(message.author.id)
        output = "I can't let you do that, <@" + str(user_id) + ">."
        await message.channel.send(output)
    
    elif message.content.startswith("$ap steal ap"):
        user_id = int(message.author.id)
        output = "That would be wrong, <@" + str(user_id) + ">."
        await message.channel.send(output)

    elif message.content.startswith("$ap gbg new"):
        temp_str = message.content.split("$ap gbg new ", 1)[1]
        board_size = temp_str.split()[0]
        enemy_ships = temp_str.split()[1]
        output = create_GBG_array(board_size, enemy_ships)
        await message.channel.send(output)

    elif message.content == "$ap gbg map":
        output = show_GBG_grid()
        await message.channel.send(output)

    elif message.content.startswith("$ap hack ap"):
        user_id = int(message.author.id)
        random_int = random.randint(1, 1000)
        output_msg = "User <@" + str(
                                        user_id
                                    ) + "> has hacked `" + str(
                                        random_int
                                    ) + " AP`, resulting in total of `0 AP` because the hack attempt was intercepted."
        output_msg = "You broke the hacking tool because you went too far... AP bot is now sad :("
        embed = discord.Embed()
        embed.color = 0x253473
        embed.add_field(name="AP broken hack tool",
                        value=output_msg,
                        inline=False)
        is_embed = True
        await message.channel.send(embed=embed)

    elif message.content.startswith("$ap_"):
        await message.channel.send(
            "Unknown command - please type `$ap help` for list of commands. Also, regular commands don't use underscore any longer."
        )

    elif message.content.startswith("$ap"):
        user_id = int(message.author.id)
        await message.channel.send(
            "Unknown command - please type `$ap help` for list of commands.")


keep_alive()
client.run(os.environ['TOKEN'])

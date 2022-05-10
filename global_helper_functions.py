import os
from replit import db

def is_admin(user_id):
    output = str(user_id) in os.environ['ADMIN']
    return output

def is_riddler(user_id):
    output = str(user_id) in os.environ['RIDDLER']
    return output

def fix_ST(user_id):
    # protected
    if is_admin(user_id):
        user_STs = db["user_STs"]
        user_APs = db["user_APs"]
        if len(user_STs) < len(user_APs):
            user_STs.append("0")
            db["user_STs"] = user_STs
            output = "STs equalized with APs successfuly."
        else:
            output = "No action required."
    else:
        output = "You are not authorized to do that."
    return output

def fix_CT(user_id):
    # protected
    if is_admin(user_id):
        user_CTs = db["user_CTs"]
        user_APs = db["user_APs"]
        if len(user_CTs) < len(user_APs):
            user_CTs.append("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            db["user_CTs"] = user_CTs
            output = "CTs equalized with APs successfuly."
        else:
            output = "No action required."
    else:
        output = "You are not authorized to do that."
    return output
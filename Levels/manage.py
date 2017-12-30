import sqlite3
from datetime import datetime


def add_user(name, user_id):
    list_of_ids = []
    list_of_user_ids = []
    user = sqlite3.connect('users.db')
    cursor = user.execute("SELECT ID, UserID from USER")
    for row in cursor:
        list_of_ids.append(row[0])
        list_of_user_ids.append(row[1])
    if len(list_of_ids) == 0:
        id_ = 0
    else:
        id_ = max(list_of_ids) + 1
    if int(user_id) not in list_of_user_ids:
        add_user_tuple((id_, name, user_id))


def add_user_tuple(values):
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        sql = "INSERT INTO USER (ID, NAME, UserID, Messages, Credits, Choice, Level, DateOfLastCredit, bought, subscribed) values (?, ?, ?, 0, 0, 0, 0, 0, 0, 0)"
        cursor.execute(sql, values)


def update_user(user_id):
    user = sqlite3.connect('users.db')
    cursor = user.execute("SELECT ID, UserID from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    c = user.cursor()
    c.execute("UPDATE USER set subscribed = ? where ID = ?", (0, int(id_)))
    user.commit()


def delete_data(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    user.execute("DELETE from USER where ID = " + str(id_) + ";")
    user.commit()


def get_data(db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, Name, UserID, Messages, Credits, Choice, Level from USER")
    return_string = ''
    for row in cursor:
        return_string = return_string + "ID = " + str(row[0]) + "\n"
        return_string = return_string + "NAME = " + str(row[1]) + "\n"
        return_string = return_string + "UserID = " + str(row[2]) + "\n"
        return_string = return_string + "Messages = " + str(row[3]) + "\n"
        return_string = return_string + "Credits = " + str(row[4]) + "\n"
        return_string = return_string + "Choice = " + str(row[5]) + "\n"
        return_string = return_string + "Level = " + str(row[6]) + "\n--------------------------------\n"
    return return_string


def add_messages(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, Messages from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            old_msgs = row[2]
        else:
            pass
    new_msgs = str(int(old_msgs) + 1)
    user.execute("UPDATE USER set Messages = ? where ID = ?", (str(new_msgs), str(id_)))
    user.commit()
    change = check_level_up(user_id)
    return change


def add_credits(user_id, amount, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, Credits from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            old_creds = row[2]
        else:
            pass
    new_creds = str(int(old_creds) + int(amount))
    now = datetime.now()
    date_var = str(now.timestamp())
    date_var = date_var.split('.')
    date_var = int(date_var[0])
    user.execute("UPDATE USER set Credits = ? where ID = ?", (str(new_creds), str(id_)))
    user.execute("UPDATE USER set DateOfLastCredit = ? where ID = ?", (str(date_var), str(id_)))
    user.commit()
    return new_creds


def check_time_for_credits(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, DateOfLastCredit, Credits from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            old_creds_time = row[2]
            credits = int(row[3])
        else:
            pass
    now = datetime.now()
    date_var = str(now.timestamp())
    date_var = date_var.split('.')
    date_var = int(date_var[0])
    if (date_var-old_creds_time) <= 86400:
        return credits
    else:
        return True


def time_till_credits(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, DateOfLastCredit from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            last_date = row[2]
        else:
            pass
    next_date = last_date + 86400
    now = datetime.now()
    date_var = str(now.timestamp())
    date_var = date_var.split('.')
    date_var = int(date_var[0])
    time = int(next_date) - int(date_var)
    if time > 7200:
        time = str(time / 3600)
        time = time.split('.')
        time = str(int(time[0])) + ' hours'
    elif time > 3600:
        time = str(time / 3600)
        time = time.split('.')
        time = str(int(time[0])) + ' hour'
    elif time > 120:
        time = str(time / 60)
        time = time.split('.')
        time = str(int(time[0])) + ' minutes'
    elif time >= 60:
        time = str(time / 60)
        time = time.split('.')
        time = str(int(time[0])) + ' minute'
    elif time <= 0:
        time = True
    elif time < 60:
        time = '1 minute'
    return time


def update_user_name(user_id, new_name, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, Name from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    try:
        user.execute("UPDATE USER set Name = ? where ID = ? ", (new_name, str(id_)))
        user.commit()
    except UnboundLocalError:
        add_user(new_name, user_id)
        update_user_name(user_id, new_name)


def get_level(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Level from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            level = row[1]
        else:
            pass
    return int(level)


def get_credits(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Credits from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            credits = row[1]
        else:
            pass
    return int(credits)


def get_messages(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Messages from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            messages = row[1]
        else:
            pass
    return int(messages)


def get_choice(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Choice from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            choice = row[1]
        else:
            pass
    return int(choice)


def get_xp(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Messages from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            messages = row[1]
        else:
            pass
    messages = int(messages)
    if messages == 0:
        xp = 0.1
    elif messages < 10:
        xp = 10 / messages
    elif 50 > messages >= 10:
        xp = 2.5 * (messages - 10)
    elif 100 > messages >= 50:
        xp = 2 * (messages - 50)
    elif 200 > messages >= 100:
        xp = messages - 100
    elif 500 > messages >= 200:
        xp = (messages - 200) / 3
    elif 1000 > messages >= 500:
        xp = (messages - 500) / 5
    elif 2000 > messages >= 1000:
        xp = (messages - 1000) / 10
    elif 5000 > messages >= 2000:
        xp = (messages - 2000) / 30
    elif 10000 > messages >= 5000:
        xp = (messages - 5000) / 50
    elif 100000 > messages >= 10000:
        xp = (messages - 10000) / 100
    elif messages > 100000:
        xp = 100
    else:
        xp = 100
    return xp


def get_total_xp(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT UserID, Messages from USER")
    for row in cursor:
        if str(row[0]) == str(user_id):
            messages = row[1]
        else:
            pass
    messages = int(messages)
    if messages == 0:
        xp = 0
    elif messages < 10:
        xp = 10 / messages
    elif 50 > messages >= 10:
        xp = 2.5 * (messages - 10) + 100
    elif 100 > messages >= 50:
        xp = 2 * (messages - 50) + 200
    elif 200 > messages >= 100:
        xp = messages - 100 + 300
    elif 500 > messages >= 200:
        xp = ((messages - 200) / 3) + 400
    elif 1000 > messages >= 500:
        xp = ((messages - 500) / 5) + 500
    elif 2000 > messages >= 1000:
        xp = ((messages - 1000) / 10) + 600
    elif 5000 > messages >= 2000:
        xp = ((messages - 2000) / 30) + 700
    elif 10000 > messages >= 5000:
        xp = ((messages - 5000) / 50) + 800
    elif 100000 > messages >= 10000:
        xp = ((messages - 10000) / 100) + 900
    elif messages > 100000:
        xp = 1000
    else:
        xp = False
    return xp


def check_level_up(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, Level, Messages from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            messages = row[3]
            level = row[2]
        else:
            pass
    change = False
    if messages >= 10 and level < 1:
        user.execute("UPDATE USER set Level = 1 where ID = ?", (str(id_),))
        user.commit()
        change = 1
    if messages >= 50 and level < 2:
        user.execute("UPDATE USER set Level = 2 where ID = ?", (str(id_),))
        user.commit()
        change = 2
    if messages >= 100 and level < 3:
        user.execute("UPDATE USER set Level = 3 where ID = ?", (str(id_),))
        user.commit()
        change = 3
    if messages >= 200 and level < 4:
        user.execute("UPDATE USER set Level = 4 where ID = ?", (str(id_),))
        user.commit()
        change = 4
    if messages >= 500 and level < 5:
        user.execute("UPDATE USER set Level = 5 where ID = ?", (str(id_),))
        user.commit()
        change = 5
    if messages >= 1000 and level < 6:
        user.execute("UPDATE USER set Level = 6 where ID = ?", (str(id_),))
        user.commit()
        change = 6
    if messages >= 2000 and level < 7:
        user.execute("UPDATE USER set Level = 7 where ID = ?", (str(id_),))
        user.commit()
        change = 7
    if messages >= 5000 and level < 8:
        user.execute("UPDATE USER set Level = 8 where ID = ?", (str(id_),))
        user.commit()
        change = 8
    if messages >= 10000 and level < 9:
        user.execute("UPDATE USER set Level = 9 where ID = ?", (str(id_),))
        user.commit()
        change = 9
    if messages >= 100000 and level < 10:
        user.execute("UPDATE USER set Level = 10 where ID = ?", (str(id_),))
        user.commit()
        change = 10
    return change


def buy_background(user_id, code, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, Credits, Choice, bought from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            _credits = row[2]
            bought = row[4]
        else:
            pass
    # user = user.cursor()
    if code == 1:
        if _credits >= 2000:
            new_credits = str(int(_credits) - 2000)
            bought = str(bought + ' 1')
            print(bought + ' ' + str(id_))
            user.execute("UPDATE USER set bought = ? where ID = ?", (bought, str(id_)))
            user.execute("UPDATE USER set credits = ? where ID = ?", (new_credits, str(id_)))
            user.execute("UPDATE USER set choice = 1 where ID = ?", (str(id_)))
            user.commit()
        else:
            return _credits
    elif code == 2:
        if _credits >= 3000:
            new_credits = str(int(_credits) - 3000)
            bought = str(bought + ' 2')
            user.execute("UPDATE USER set bought = ? where ID = ?", (bought, str(id_)))
            user.execute("UPDATE USER set credits = ? where ID = ?", (new_credits, str(id_)))
            user.execute("UPDATE USER set choice = 2 where ID = ?", (str(id_)))
            user.commit()
        else:
            return _credits
    elif code == 3:
        if _credits >= 3500:
            new_credits = str(int(_credits) - 3500)
            bought = str(bought + ' 3')
            user.execute("UPDATE USER set bought = ? where ID = ?", (bought, str(id_)))
            user.execute("UPDATE USER set credits = ? where ID = ?", (new_credits, str(id_)))
            user.execute("UPDATE USER set choice = 3 where ID = ?", (str(id_)))
            user.commit()
        else:
            return _credits
    elif code == 4:
        if _credits >= 4000:
            new_credits = str(int(_credits) - 4000)
            bought = str(bought + ' 4')
            user.execute("UPDATE USER set bought = ? where ID = ?", (bought, str(id_)))
            user.execute("UPDATE USER set credits = ? where ID = ?", (new_credits, str(id_)))
            user.execute("UPDATE USER set choice = 4 where ID = ?", (str(id_)))
            user.commit()
        else:
            return _credits
    elif code == 5:
        if _credits >= 5000:
            new_credits = str(int(_credits) - 5000)
            bought = str(bought + ' 5')
            user.execute("UPDATE USER set bought = ? where ID = ?", (bought, str(id_)))
            user.execute("UPDATE USER set credits = ? where ID = ?", (new_credits, str(id_)))
            user.execute("UPDATE USER set choice = 5 where ID = ?", (str(id_)))
            user.commit()
        else:
            return _credits
    else:
        return False


def bought_(user_id, choice, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, bought from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            bought = row[2]
        else:
            pass
    bought = bought.split(' ')
    if str(choice) in bought:
        return True
    else:
        return False


def set_choice(user_id, choice, db_name='users.db'):
    try:
        user = sqlite3.connect(db_name)
        cursor = user.execute("SELECT ID, UserID from USER")
        for row in cursor:
            if str(row[1]) == str(user_id):
                id_ = row[0]
            else:
                pass
        user.execute("UPDATE USER set Choice = ? where ID = ?", (str(choice), str(id_)))
        user.commit()
        return True
    except:
        return False


def unsubscribe(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, subscribed from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            subscribed = row[2]
        else:
            pass
    if subscribed != 0 or subscribed != 1:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(1), str(id_)))
        user.commit()
        return True
    elif subscribed == 0:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(1), str(id_)))
        user.commit()
        return True
    elif subscribed == 1:
        return False
    else:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(1), str(id_)))
        user.commit()
        return True


def subscribe(user_id, db_name='users.db'):
    user = sqlite3.connect(db_name)
    cursor = user.execute("SELECT ID, UserID, subscribed from USER")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            subscribed = row[2]
        else:
            pass
    if subscribed != 0 or subscribed != 1:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(0), str(id_)))
        user.commit()
        return True
    elif subscribed == 0:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(0), str(id_)))
        user.commit()
        return True
    elif subscribed == 1:
        return False
    else:
        user.execute("UPDATE USER set subscribed = ? where ID = ?", (str(0), str(id_)))
        user.commit()
        return True




# Add Data
# add_user('name', 2345678765678)

# Add Messages
# add_messages(2345678765678)

# Delete data
# delete_data(2345678765678)


# Print Data

# string = get_data('users.db')
# if string == '':
#     string = 'No data is in the table'
# print(string)

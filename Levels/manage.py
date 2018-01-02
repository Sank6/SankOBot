import psycopg2
from urllib import parse
import os
from datetime import datetime

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ.get("DATABASE_URL"))


def add_user(name, user_id):
    list_of_ids = []
    list_of_user_ids = []
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID from USERS")
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
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    sql = "INSERT INTO USERS (ID, NAME, UserID, Messages, Credits, Choice, Level, DateOfLastCredit, bought, subscribed) values (%s, %s, %s, 0, 0, 0, 0, 0, 0, 0)"
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def update_user(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (0, int(id_)))
    conn.commit()
    cursor.close()
    conn.close()


def delete_data(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    cursor.execute("DELETE from USERS where ID = " + str(id_) + ";")
    conn.commit()
    cursor.close()
    conn.close()


def get_data():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Name, UserID, Messages, Credits, Choice, Level from USERS")
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


def add_messages(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, Messages from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            old_msgs = row[2]
        else:
            pass
    new_msgs = str(int(old_msgs) + 1)
    cursor.execute("UPDATE USERS set Messages = %s where ID = %s", (str(new_msgs), str(id_)))
    conn.commit()
    cursor.close()
    conn.close()
    change = check_level_up(user_id)
    return change


def add_credits(user_id, amount):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, Credits from USERS")
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
    cursor.execute("UPDATE USERS set Credits = %s where ID = %s", (str(new_creds), str(id_)))
    cursor.execute("UPDATE USERS set DateOfLastCredit = %s where ID = %s", (str(date_var), str(id_)))
    conn.commit()
    cursor.close()
    conn.close()
    return new_creds


def check_time_for_credits(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, DateOfLastCredit, Credits from USERS")
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


def time_till_credits(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, DateOfLastCredit from USERS")
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


def update_user_name(user_id, new_name):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, Name from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
        else:
            pass
    try:
        cursor.execute("UPDATE USERS set Name = %s where ID = %s ", (new_name, str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
    except UnboundLocalError:
        add_user(new_name, user_id)
        update_user_name(user_id, new_name)


def get_level(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Level from USERS")
    for row in cursor:
        if str(row[0]) == str(user_id):
            level = row[1]
        else:
            pass
    return int(level)


def get_credits(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Credits from USERS")
    for row in cursor:
        if str(row[0]) == str(user_id):
            credits = row[1]
        else:
            pass
    return int(credits)


def get_messages(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Messages from USERS")
    for row in cursor:
        if str(row[0]) == str(user_id):
            messages = row[1]
        else:
            pass
    return int(messages)


def get_choice(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Choice from USERS")
    for row in cursor:
        if str(row[0]) == str(user_id):
            choice = row[1]
        else:
            pass
    return int(choice)


def get_xp(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Messages from USERS")
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


def get_total_xp(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Messages from USERS")
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


def check_level_up(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, Level, Messages from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            messages = row[3]
            level = row[2]
        else:
            pass
    change = False
    if messages >= 10 and level < 1:
        cursor.execute("UPDATE USERS set Level = 1 where ID = %s", (str(id_),))
        change = 1
    if messages >= 50 and level < 2:
        cursor.execute("UPDATE USERS set Level = 2 where ID = %s", (str(id_),))
        change = 2
    if messages >= 100 and level < 3:
        cursor.execute("UPDATE USERS set Level = 3 where ID = %s", (str(id_),))
        change = 3
    if messages >= 200 and level < 4:
        cursor.execute("UPDATE USERS set Level = 4 where ID = %s", (str(id_),))
        change = 4
    if messages >= 500 and level < 5:
        cursor.execute("UPDATE USERS set Level = 5 where ID = %s", (str(id_),))
        change = 5
    if messages >= 1000 and level < 6:
        cursor.execute("UPDATE USERS set Level = 6 where ID = %s", (str(id_),))
        change = 6
    if messages >= 2000 and level < 7:
        cursor.execute("UPDATE USERS set Level = 7 where ID = %s", (str(id_),))
        change = 7
    if messages >= 5000 and level < 8:
        cursor.execute("UPDATE USERS set Level = 8 where ID = %s", (str(id_),))
        change = 8
    if messages >= 10000 and level < 9:
        cursor.execute("UPDATE USERS set Level = 9 where ID = %s", (str(id_),))
        change = 9
    if messages >= 100000 and level < 10:
        cursor.execute("UPDATE USERS set Level = 10 where ID = %s", (str(id_),))
        change = 10
    conn.commit()
    cursor.close()
    conn.close()
    return change


def buy_background(user_id, code):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, Credits, Choice, bought from USERS")
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
            cursor.execute("UPDATE USERS set bought = %s where ID = %s", (bought, str(id_)))
            cursor.execute("UPDATE USERS set credits = %s where ID = %s", (new_credits, str(id_)))
            cursor.execute("UPDATE USERS set choice = 1 where ID = %s", (str(id_)))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return _credits
    elif code == 2:
        if _credits >= 3000:
            new_credits = str(int(_credits) - 3000)
            bought = str(bought + ' 2')
            cursor.execute("UPDATE USERS set bought = %s where ID = %s", (bought, str(id_)))
            cursor.execute("UPDATE USERS set credits = %s where ID = %s", (new_credits, str(id_)))
            cursor.execute("UPDATE USERS set choice = 2 where ID = %s", (str(id_)))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return _credits
    elif code == 3:
        if _credits >= 3500:
            new_credits = str(int(_credits) - 3500)
            bought = str(bought + ' 3')
            cursor.execute("UPDATE USERS set bought = %s where ID = %s", (bought, str(id_)))
            cursor.execute("UPDATE USERS set credits = %s where ID = %s", (new_credits, str(id_)))
            cursor.execute("UPDATE USERS set choice = 3 where ID = %s", (str(id_)))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return _credits
    elif code == 4:
        if _credits >= 4000:
            new_credits = str(int(_credits) - 4000)
            bought = str(bought + ' 4')
            cursor.execute("UPDATE USERS set bought = %s where ID = %s", (bought, str(id_)))
            cursor.execute("UPDATE USERS set credits = %s where ID = %s", (new_credits, str(id_)))
            cursor.execute("UPDATE USERS set choice = 4 where ID = %s", (str(id_)))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return _credits
    elif code == 5:
        if _credits >= 5000:
            new_credits = str(int(_credits) - 5000)
            bought = str(bought + ' 5')
            cursor.execute("UPDATE USERS set bought = %s where ID = %s", (bought, str(id_)))
            cursor.execute("UPDATE USERS set credits = %s where ID = %s", (new_credits, str(id_)))
            cursor.execute("UPDATE USERS set choice = 5 where ID = %s", (str(id_)))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return _credits
    else:
        return False


def bought_(user_id, choice):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, bought from USERS")
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


def set_choice(user_id, choice):
    try:
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT ID, UserID from USERS")
        for row in cursor:
            if str(row[1]) == str(user_id):
                id_ = row[0]
            else:
                pass
        cursor.execute("UPDATE USERS set Choice = %s where ID = %s", (str(choice), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except:
        return False


def unsubscribe(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, subscribed from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            subscribed = row[2]
        else:
            pass
    if subscribed != 0 or subscribed != 1:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(1), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    elif subscribed == 0:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(1), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    elif subscribed == 1:
        return False
    else:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(1), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True


def subscribe(user_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, UserID, subscribed from USERS")
    for row in cursor:
        if str(row[1]) == str(user_id):
            id_ = row[0]
            subscribed = row[2]
        else:
            pass
    if subscribed != 0 or subscribed != 1:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(0), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    elif subscribed == 0:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(0), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    elif subscribed == 1:
        return False
    else:
        cursor.execute("UPDATE USERS set subscribed = %s where ID = %s", (str(0), str(id_)))
        conn.commit()
        cursor.close()
        conn.close()
        return True


# Add Data
# add_user('name', 1)

# Add Messages
# add_messages(2345678765678)

# Delete data
# delete_data(1)


# Print Data

# string = get_data()
# if string == '':
#     string = 'No data is in the table'
# print(string)

import sqlite3


def add_server(name, server_id, invite_link, member_count):
    list_of_ids = []
    list_of_server_ids = []
    user = sqlite3.connect('server_s.db')
    cursor = user.execute("SELECT ID, SERVER_ID from SERVERS")
    for row in cursor:
        list_of_ids.append(row[0])
        list_of_server_ids.append(row[1])
    if len(list_of_ids) == 0:
        id_ = 0
    else:
        try:
            first_value = next(val for val in range(len(list_of_ids)) if val not in list_of_ids)
        except StopIteration:
            first_value = len(list_of_ids) + 1
        id_ = first_value
    if int(server_id) not in list_of_server_ids:
        add_server_tuple((id_, name, server_id, invite_link, member_count))


def add_server_tuple(values):
    with sqlite3.connect('server_s.db') as db:
        cursor = db.cursor()
        sql = "INSERT INTO SERVERS (ID, NAME, SERVER_ID, INVITE, MEMBERS, REMOVED) values (?, ?, ?, ?, ?, 0)"
        cursor.execute(sql, values)


def removed_from_server(server_id):
    user = sqlite3.connect('server_s.db')
    cursor = user.execute("SELECT ID, SERVER_ID from SERVERS")
    for row in cursor:
        if str(row[1]) == str(server_id):
            id_ = row[0]
        else:
            pass
    cursor.execute('''UPDATE SERVERS set REMOVED = ? where ID = ? ''',
                   ("1", str(id_)))
    user.commit()

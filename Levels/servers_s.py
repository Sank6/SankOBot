import psycopg2
from urllib import parse
import os

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ.get("DATABASE_URL"))


def add_server(name, server_id, invite_link, member_count):
    list_of_ids = []
    list_of_server_ids = []
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, SERVER_ID from SERVERS")
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
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    sql = """
     INSERT INTO servers (ID, NAME, SERVER_ID, INVITE, MEMBERS, REMOVED)
     VALUES (%s, %s, %s, %s, %s, 0);
     """
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def removed_from_server(server_id):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("SELECT ID, SERVER_ID from SERVERS")
    for row in cursor:
        if str(row[1]) == str(server_id):
            id_ = row[0]
        else:
            pass
    cursor.execute("UPDATE SERVERS set REMOVED = %s where ID = %s ", ("1", str(id_)))
    # cursor.execute("DELETE from servers where ID = %s", (str(id_,)))
    conn.commit()
    cursor.close()
    conn.close()



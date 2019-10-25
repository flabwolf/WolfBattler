import sqlite3
import cgi
import cgitb
import sys
import json

cgitb.enable()
print("Content-Type: text/html\n\n")
form = cgi.FieldStorage()

# データベースの作成


def save_room():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE rooms(id INTEGER PRIMARY KEY,name text UNIQUE, setting INTEGER, player_num INTEGER DEFAULT 0, port INTEGER)')
    c.execute(
        'CREATE TABLE players(id INTEGER PRIMARY KEY,name text UNIQUE, agent_id INTEGER, room_id INTEGER)')
    conn.commit()
    conn.close()


# save_room()
# プレイヤーの作成


def create_player():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    player_name = form.getfirst("player_name")
    # player_name = "中原"
    c.execute("INSERT INTO players (name) VALUES ('%s')" % player_name)
    # c.execute('INSERT INTO players (name) VALUES ("中原")')
    conn.commit()
    conn.close()

# ルーム作成


def create_room():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_name = form.getfirst("room_name")
    c.execute("INSERT INTO rooms (name) VALUES ('%s')" % room_name)
    idx = list(c.execute("SELECT id FROM rooms WHERE name='%s'" %
                         room_name))[0][0]
    port = idx + 79
    c.execute("UPDATE rooms SET port=%d WHERE name='%s'" % (port, room_name))
    conn.commit()
    conn.close()

# ルーム参加


def join_room():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_name = form.getfirst("room_name")
    player_name = form.getfirst("player_name")
    room_id = list(
        c.execute("SELECT id FROM rooms WHERE name='%s'" % room_name))[0][0]
    player_num = list(
        c.execute("SELECT player_num FROM rooms WHERE name='%s'" % room_name))[0][0]
    player_num += 1
    c.execute("UPDATE rooms SET player_num=%d WHERE name='%s'" %
              (player_num, room_name))
    agent_id_list = [1, 2, 3, 4, 5]
    agent_ids = []
    a = list(
        c.execute("SELECT agent_id FROM players WHERE room_id=%d" % room_id))
    for i in a:
        agent_ids.append(i[0])
    for agent_id in agent_ids:
        if not agent_id in agent_id_list:
            c.execute("UPDATE players SET agent_id=%d, room_id=%d WHERE name='%s'" %
                      (agent_id, room_id, player_name))
            break
    conn.commit()
    conn.close()

# プレイヤー情報を取得する


def get_player_info():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    player_info = []
    player_infos = list(c.execute("SELECT * FROM players"))
    for i in player_infos:
        player_info.append(i)
    conn.commit()
    conn.close()
    print(json.dumps(player_info))

# ルーム情報を取得する


def get_room_info():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_info = []
    room_infos = list(c.execute("SELECT * FROM rooms"))
    for i in room_infos:
        room_info.append(i)
    conn.commit()
    conn.close()
    print(json.dumps(room_info))


# ルーム退出


def exit_room():
    if "room_name" in form:
        conn = sqlite3.connect('db/wolf_battler.db')
        c = conn.cursor()
        room_name = form.getfirst("room_name")
        player_name = form.getfirst("player_name")
        c.execute(
            "UPDATE players SET room_id=NULL, agent_id=NULL WHERE name='%s'" % player_name)
        player_num = list(
            c.execute("SELECT player_num FROM rooms WHERE name='%s'" % room_name))[0][0]
        player_num -= 1
        c.execute("UPDATE rooms SET player_num=%d" % (player_num))
        conn.commit()
        conn.close()
        if player_num == 0:
            del_room(room_name)


# ルーム削除


def del_room(room_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute("DELETE FROM rooms WHERE name='%s'" % room_name)
    conn.commit()
    conn.close()

# プレイヤーの削除


def del_player(player_name):
    exit_room()
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE name='%s'" % player_name)
    conn.commit()
    conn.close()


# main関数部分
if "func" in form:
    func = form.getfirst("func")
    if func == "create_room":
        create_room()
    elif func == "create_player":
        create_player()
    elif func == "join_room":
        join_room()
    elif func == "exit_room":
        exit_room()
    elif func == "get_player_info":
        get_player_info()
    elif func == "get_room_info":
        get_room_info()
    elif func == "del_player":
        player_name = form.getfirst("player_name")
        del_player(player_name)
    elif func == "del_room":
        room_name = form.getfirst("room_name")
        del_room(room_name)

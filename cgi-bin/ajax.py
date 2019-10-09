import sqlite3
import cgi
import cgitb
import sys
import json

cgitb.enable()
print("Content-Type: text/html\n\n")

# データベースの作成


def save_room():
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE rooms(id INTEGER PRIMARY KEY,name text UNIQUE, setting INTEGER)')
    c.execute(
        'CREATE TABLE players(id INTEGER PRIMARY KEY,name text UNIQUE, agent_id INTEGER, room_id INTEGER)')
    conn.commit()
    conn.close()


# save_room()

# roomsに作成したルームを追加


def create_room(room_name, setting=60):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute("INSERT INTO rooms (name,setting) VALUES ('%s',%d)" %
              (room_name, setting))
    conn.commit()
    conn.close()
    ret = {"room_name": room_name}
    print(json.dumps(ret))

# playersに作成したプレイヤーを追加


def create_player(player_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES ('%s')" % player_name)
    conn.commit()
    conn.close()
    ret = json.dumps({"player_name": player_name})
    print(ret)

# playersに参加したroom_idを追加する


def join_room(room_name, player_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_id = list(
        c.execute("SELECT id FROM rooms WHERE name='%s'" % room_name))[0][0]
    c.execute("UPDATE players SET room_id=%d WHERE name='%s'" %
              (room_id, player_name))
    agent_num = [1, 2, 3, 4, 5]
    agent_ids = c.execute(
        "SELECT agent_id FROM players WHERE room_id=%d" % room_id)
    for i in agent_ids:
        if i[0] != None:
            agent_num.remove(i[0])
    if agent_num:
        c.execute("UPDATE players SET agent_id=%d WHERE name='%s'" %
                  (agent_num[0], player_name))
    conn.commit()
    conn.close()

# ルームを退出する


def exit_room(room_name, player_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_id = list(
        c.execute("SELECT id FROM rooms WHERE name='%s'" % room_name))[0][0]
    c.execute("UPDATE players SET agent_id=NULL, room_id=NULL WHERE room_id=%d AND name='%s'" % (
        room_id, player_name))
    conn.commit()
    conn.close()
    del_room(room_name)


def del_room(room_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    room_id = list(
        c.execute("SELECT id FROM rooms WHERE name='%s'" % room_name))[0][0]
    num_player = list(
        c.execute("SELECT * FROM players WHERE room_id=%d" % room_id))
    if len(num_player) == 0:
        c.execute("DELETE FROM rooms WHERE name='%s'" % room_name)
    conn.commit()
    conn.close()


def del_player(player_name, room_name=False):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE name='%s'" % player_name)
    conn.commit()
    conn.close()
    if room_name != False:
        del_room(room_name)


# main関数部分
form = cgi.FieldStorage()
print(form.getfirst("room_name"), file=sys.stderr)
if "func" in form:
    func = form.getfirst("func")
    if func == "create_room":
        room_name = form.getfirst("room_name")
        create_room(room_name)
    elif func == "create_player":
        player_name = form.getfirst("player_name")
        create_player(player_name)
    elif func == "join_room":
        room_name = form.getfirst("room_name")
        player_name = form.getfirst("player_name")
        join_room(room_name, player_name)
    elif func == "exit_room":
        room_name = form.getfirst("room_name")
        player_name = form.getfirst("player_name")
        exit_room(room_name, player_name)
    elif func == "del_player":
        player_name = form.getfirst("player_name")
        if "room_name" in form:
            room_name = form.getfirst("room_name")
            del_player(player_name, room_name)
        else:
            del_player(player_name)

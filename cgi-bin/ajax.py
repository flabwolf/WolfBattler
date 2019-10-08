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
        'CREATE TABLE players(id INTEGER PRIMARY KEY,name text UNIQUE, agent INTEGER, room_id INTEGER)')
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
    conn.commit()
    conn.close()

# プレイヤー名を取得


def get_player_name(room_name):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    player_name = list(c.execute(
        "SELECT players.name FROM players INNER join rooms ON players.room_id = rooms.id and players.agent IS NULL"))[0][0]
    agent_num = [1, 2, 3, 4, 5]
    agent_ids = c.execute(
        "SELECT agent FROM players INNER join rooms ON players.room_id = rooms.id and rooms.name='%s'" % room_name)
    for i in agent_ids:
        if i[0] != None:
            agent_num.remove(i[0])
    if agent_num:
        c.execute("UPDATE players SET agent=%d WHERE name='%s'" %
                  (agent_num[0], player_name))
    ret = {"player_name": player_name}
    conn.close()
    print(json.dumps(ret))


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
    elif func == "get_player_name":
        room_name = form.getfirst("room_name")
        get_player_name(room_name)

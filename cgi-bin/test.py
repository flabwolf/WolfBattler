import sqlite3
import json


def create_player(agent, name="Agent"):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    ret = {}
    rooms = list(c.execute("SELECT name FROM rooms"))
    # print(list(rooms))
    for i in rooms:
        print(i)

        room_id = list(
            c.execute("SELECT id FROM rooms WHERE name='%s'" % i[0]))[0][0]
        num_player = list(
            c.execute("SELECT * FROM players WHERE room_id=%d" % room_id))
        ret[i[0]] = len(num_player)
    conn.close()
    print(ret)


create_player(1, "nakahara")

print("hello world")
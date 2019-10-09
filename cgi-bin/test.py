import sqlite3


def create_player(agent, name="Agent"):
    conn = sqlite3.connect('db/wolf_battler.db')
    c = conn.cursor()
    player_name = name
    agent_ids = []
    ids = [1, 2, 3, 4, 5]
    room_name = "神"
    a = c.execute(
        "SELECT players.name FROM players INNER join rooms ON players.room_id = rooms.id AND players.agent IS NULL AND rooms.name='%s'" % room_name)
    for i in a:
        print(i)

    # conn.commit()
    conn.close()


create_player(1, "nakahara")

from sqlite3 import connect, Connection, Cursor

db: Connection = connect('server.db')
sql: Cursor = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    id INTEGER,
    ingame INTEGER);
""")

sql.execute("""CREATE TABLE IF NOT EXISTS users_stats (
    id INTEGER,  
    attempts INTEGER,
    games_count INTEGER,
    games_win INTEGER,
    rand_num INTEGER);
""")

db.commit()


def check_user_in_table(id: int) -> bool:
    sql.execute("SELECT * FROM users;")
    users = sql.fetchall()

    for user in users:
        if user[1] == id:
            return True
            break
    return False


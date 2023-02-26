from sqlite3 import connect, Connection, Cursor
from random import randint
from aiogram import types

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
    """
    this func will return true if user in users else false
    id: int - user id
    return: bool - true if user in users else false
    """
    sql.execute(f"SELECT * FROM users WHERE id = {id};")
    user = sql.fetchone()

    if user is None:
        return False
    return True


def append_users(message: types.Message) -> None:
    """
    this func will add user to users table
    username: str - user name
    id: int - user id
    ingame: int - 0 if not in game else 1
    return: None
    """
    n = randint(0, 100)
    sql.execute("INSERT INTO users (username, id, ingame) values (?, ?, ?)", (message.from_user.username, message.from_id, 0))
    sql.execute("INSERT INTO users_stats (id, attempts, games_count, games_win, rand_num) values (?, ?, ?, ?, ?)", (message.from_id, 7, 0, 0, n))
    db.commit()


def change_ingame(id: int) -> None:
    if check_ingame(id):
        with db:
            sql.execute(f"UPDATE users SET ingame = 0 WHERE id = {id}")
    else:
        sql.execute(f"SELECT * from users_stats WHERE id = {id}")
        user = sql.fetchone()
        with db:
            sql.execute(f"UPDATE users_stats SET rand_num = {randint(0, 100)}")
            sql.execute(f"UPDATE users_stats SET games_count = {user[2]+1}")
            sql.execute(f"UPDATE users SET ingame = 1 WHERE id = {id}")



def check_ingame(id: int) -> bool:
    sql.execute(f"SELECT * FROM users WHERE id = {id}")
    user = sql.fetchone()

    if user:
        if user[2]:
            return True
    return False


def game(message: types.Message, n):
    attempts = sql.execute(f"SELECT attempts FROM users_stats WHERE id = {message.from_id}").fetchone()[0]
    games_win = sql.execute(f"SELECT games_win FROM users_stats WHERE id = {message.from_id}").fetchone()[0]
    rand_num = sql.execute(f"SELECT rand_num FROM users_stats WHERE id = {message.from_id}").fetchone()[0]
    
    if attempts > 0:
        attempts -= 1
        if n == rand_num:
            games_win += 1
            sql.execute(f"UPDATE users_stats SET attempts = {7}")
            sql.execute(f"UPDATE users_stats SET games_win = {games_win}")
            change_ingame(message.from_id)
            return "win"
        else:
            sql.execute(f"UPDATE users_stats SET attempts = {attempts}")
            if rand_num > n:
                return [attempts, True]
            else:
                return [attempts, False]
    else:
        return "defeat"

        
    """if rand_num == n:
        sql.execute(f"UPDATE users_stats SET games_win = {games_win+1}")
        sql.execute(f"UPDATE users_stats SET attempts = {7}")
        return True
    else:
        sql.execute(f"UPDATE users_stats SET attempts = {attempts-1}")
        if attempts-1 <= 0:
            sql.execute(f"UPDATE users_stats SET attempts = {7}")
            return False
        else:
            return True"""
    

def tests():
    id = 2120080409

    sql.execute(f"SELECT username FROM users WHERE id = {id}")
    users = sql.fetchone()
    print(users[0])

    attempts = sql.execute(f"SELECT * FROM users_stats WHERE id = {id}").fetchone()[0]



if __name__ == "__main__":
    tests()
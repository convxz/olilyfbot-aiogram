""" my first bot in telegram """

from os import getenv
from sqlite3 import connect, Connection, Cursor
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
BOT_TOKEN: str = str(getenv('BOT_TOKEN'))

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

db: Connection = connect('server.db')
sql: Cursor = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    id INTEGER,
    ingame INTEGER);
""")
db.commit()


async def process_echo_message(message: types.Message) -> None:
    # This func will send you your text message
    await message.answer(message.text)


async def process_start_command(message: types.Message) -> None:
    # This func will reply to command 'start'
    sql.execute("SELECT * FROM users;")
    res = sql.fetchall()

    a = 0
    for i in range(len(res)):
        if res[i][1] == message.from_user.id:
            a = 1
            break

    if not(a):
        sql.execute(f'INSERT INTO users (username, id, ingame) values (?, ?, ?)', (message.from_user.username, message.from_user.id, 1))
        db.commit()

    await message.answer('Hello!\n\nThis bot was created by kartosha, you can give him motivation to work so much more:\n\n2202205347399922')


if __name__ == '__main__':
    dp.register_message_handler(process_start_command, commands=['start'])
    executor.start_polling(dp, skip_updates=True)

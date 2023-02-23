""" my first bot in telegram """

from os import getenv
from sqlite3 import connect, Connection, Cursor
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from db_help import check_user_in_table, db, sql

load_dotenv()
BOT_TOKEN: str = str(getenv("BOT_TOKEN"))

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)


async def process_echo_message(message: types.Message) -> None:
    # This func will send you your text message
    await message.answer(message.text)


async def process_start_command(message: types.Message) -> None:
    # This func will reply to command 'start'

    if not(check_user_in_table(message.from_id)):
        sql.execute(f"INSERT INTO users (username, id, ingame) values (?, ?, ?)", (message.from_user.username, message.from_user.id, 1))
        db.commit()

    await message.answer("Hello!\n\nThis bot was created by kartosha, you can give him motivation to work so much more:\n\n2202205347399922")


if __name__ == "__main__":
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(process_echo_message, content_types=["text"])
    executor.start_polling(dp, skip_updates=True)

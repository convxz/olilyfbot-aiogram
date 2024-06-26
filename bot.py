from os import getenv, remove
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from db_help import check_user_in_table, append_users, check_ingame
from db_help import change_ingame, game
from cats import cat
load_dotenv()
BOT_TOKEN: str = str(getenv("BOT_TOKEN"))

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)


async def process_start_command(message: types.Message) -> None:
    # This func will reply to command 'start'
    id = message.from_id

    if not(check_user_in_table(id)):
        append_users(message)

    if not(check_ingame(id)):
        await message.answer("Hello!\n\nThis bot was created by kartosha, you can give him motivation to work so much more:\n\n2202205347399922")
    else:
        await message.answer("you are in game.")


async def process_echo_message(message: types.Message) -> None:
    # This func will send you your text message
    id = message.from_id
    if check_ingame(id):
        try:
            n = int(message.text)
            res = game(message, n)
            if res == "win":
                await message.answer("you win!")
            elif res == "defeat":
                await message.answer("defeat")
            else:
                if res[1]:
                    await message.answer(f"not right, bigger \nattempts: {res[0]}")
                else:
                    await message.answer(f"not right, smaller \nattempts: {res[0]}")

        except ValueError:
            await message.answer("it's not right data type. please, write num")
    else:
        await message.answer(message.text)


async def process_start_game(message: types.Message) -> None:
    if check_ingame(message.from_id):
        await message.answer("you are in game.")
    else:
        await message.answer("alright, welcome to game!")
        change_ingame(message.from_id)


async def process_cancel_game(message: types.Message) -> None:
    if check_ingame(message.from_id):
        await message.answer("you are not in game already.")
        change_ingame(message.from_id)
    else:
        await message.answer("you are not in game.")


async def process_send_cats(message: types.Message) -> None:
    cat(BOT_TOKEN, message.from_id)

    
if __name__ == "__main__":
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(process_start_game, commands=["start_game"])
    dp.register_message_handler(process_cancel_game, commands=["cancel"])
    dp.register_message_handler(process_send_cats, commands=["meow"])
    dp.register_message_handler(process_echo_message, content_types=["text"])
    executor.start_polling(dp, skip_updates=True)

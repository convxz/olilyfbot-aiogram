from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
BOT_TOKEN: str = getenv('BOT_TOKEN')

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)


async def process_start_command(message: types.Message) -> None:
    """
    This func will reply to command 'start'
    """
    await message.answer('Hello!\n\nThis bot was created by kartosha, you can give him motivation to work so much more:\n\n2202205347399922')


if __name__ == '__main__':
    dp.register_message_handler(process_start_command, commands=['start'])
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio
token = '1974044321:AAHFWyRqn05-wTDgx8PzBMU9Cr_M6AYPQns'

async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.reply(f'Привет {message.from_user.first_name}. Рад тебя видеть!')

async def start():
    bot = Bot(token=token)

    dp = Dispatcher()
    dp.message.register(get_start)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
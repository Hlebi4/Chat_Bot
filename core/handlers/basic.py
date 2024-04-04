from aiogram import Bot
from aiogram.types import Message

async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.reply(f'Привет {message.from_user.first_name}. Рад тебя видеть!')
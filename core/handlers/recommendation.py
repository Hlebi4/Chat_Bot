from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.untils.statesform import StepsForm
from main import get_recommendations
from main import get_similar


async def get_recommendatrion(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, укажите фильм, который вы смотрели последним')
    await state.set_state(StepsForm.GET_FILM)

async def expectation_rec(message: Message, state: FSMContext):
    await message.answer((f'Указанный фильм:\r\n{message.text}\r\nТеперь дайте ему оценку от 1 до 5'))
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_RATING)

async def get_rating(message: Message, state: FSMContext):
    await message.answer((f'Ваш рейтинг:\r\n{message.text}\r\nПодбираем подходящие...'))
    await state.update_data(rating=message.text)
    context_data = await state.get_data()
    #rec = get_recommendations(context_data.get('name'))
    rait = get_similar(context_data.get('name'), int(context_data.get('rating')))
    #await message.answer(rec)
    await message.answer(rait)
    await message.answer((f'Если вам потребуется новая рекоммендация - обращайтесь :)'))
    await state.clear()
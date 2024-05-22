from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.untils.statesform import StepsForm
from main import get_recommendations


async def get_recommendatrion(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, укажите фильм, который вам понравился')
    await state.set_state(StepsForm.GET_FILM)

async def expectation_rec(message: Message, state: FSMContext):
    await message.answer((f'Указанный фильм:\r\n{message.text}\r\nПодбираем похожие...'))
    await state.update_data(name=message.text)
    context_data = await state.get_data()
    rec = get_recommendations(context_data.get('name'))
    await message.answer(rec)
    await message.answer((f'Если вам потребуется новая рекоммендация - обращайтесь :)'))
    await state.clear()
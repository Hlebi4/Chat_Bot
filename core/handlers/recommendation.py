from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.untils.statesform import StepsForm

async def get_recommendatrion(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, укажите фильм, который вам понравился')
    await state.set_state(StepsForm.GET_FILM)

async def expectation_rec(message: Message):
    await message.answer((f'Указанный фильм:\r\n{message.text}\r\nПодбираем похожий'))
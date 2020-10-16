import logging
from quizzer import Quiz
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token='1102746633:AAH2i3PRyzXa4AzKNzzoQgM8P20gLmXK4e8')
dp = Dispatcher(bot)

quizzes_database = {}
quizzes_owners = {}


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Создать викторину"),
                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ))
    poll_keyboard.add(types.KeyboardButton(text='Отмена'))
    await message.answer('Нажмите на кнопку и создайте викторину',
                         reply_markup=poll_keyboard)

@dp.message_handler(lambda message: message.text == 'отмена')
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer('Действие отменено', reply_markup=remove_keyboard)

@dp.message_handler(content_types=['poll'])
async def msg_with_poll(message: types.Message):
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []
    
    if message.poll.type != 'quiz':
        await message.reply('Принимаю только викторины')
        return

    quizzes_database[str(message.from_user.id)].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id
    ))
    quizzes_owners[message.poll.id] = str(message.from_user.id)

    await message.reply(
        f"Викторина сохранена. Общее число сохраненных викторин - {len(quizzes_database[str(message.from_user.id)])}"
    )
import os
import aiogram
import random
from aiogram import types
from aiogram.dispatcher.filters import Command
from gtts import gTTS
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.types import InputFile

bot = aiogram.Bot(token=" ") #@BotFather
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

class CaptchaState(StatesGroup):
    waiting_for_captcha = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    russian_words = [
    'абажур', 'авиатор', 'агент', 'адмирал', 'азарт', 'аккорд', 'алкоголь', 'алмаз', 'алый', 'аметист',
    'ангел', 'ангина', 'анекдот', 'апостол', 'арабский', 'арбуз', 'арена', 'артист', 'арфа', 'архив',
    'аскет', 'атака', 'атлас', 'атом', 'аукцион', 'аура', 'афера', 'аэропорт', 'бабушка', 'багаж',
    'бадминтон', 'балет', 'бамбук', 'банан', 'банк', 'баня', 'баран', 'бард', 'баржа', 'барин',
    'барон', 'барсук', 'батарея', 'бахрома', 'башня', 'баян', 'бегемот', 'бедро', 'бежать', 'бездна',
    'бекон', 'белка', 'белый', 'бензин', 'береза', 'беседа', 'бетон', 'биатлон', 'библиотека', 'бизнес',
    'билет', 'бинокль', 'биология', 'биржа', 'бисер', 'битва', 'благо', 'блеск', 'блин', 'блокнот',
    'блондинка', 'блюдо', 'бляха', 'бобер', 'богатый', 'бодрый', 'боевик', 'бокал', 'больница', 'бордюр',
    'борщ', 'ботинок', 'бочка', 'бояться', 'браслет', 'бревно', 'бриллиант', 'бритва', 'бронза', 'бросать',
    'брызги', 'брюки', 'бублик', 'бугор', 'будильник', 'буква', 'бульвар', 'бумага', 'бунт', 'буря',
]

    captcha_words = random.sample(russian_words, 1)
    captcha_audio_path = "captcha.oog"
    captcha_audio = gTTS(" ".join(captcha_words), lang="ru")
    captcha_audio.save(captcha_audio_path)

    with open(captcha_audio_path, "rb") as f:
        captcha_voice = types.InputFile(f)
        await message.answer_voice(captcha_voice, caption="Введите слово, которое вы услышали в данном голосовом сообщении)")

    await state.update_data(captcha_words=captcha_words)
    await CaptchaState.waiting_for_captcha.set()
    dp.register_message_handler(captcha_check, state=CaptchaState.waiting_for_captcha, content_types=types.ContentTypes.TEXT)

async def captcha_check(message: types.Message, state: FSMContext):
    captcha_words = (await state.get_data()).get("captcha_words")
    user_words = message.text.strip().split()
    if ' '.join(user_words).lower() == ' '.join(captcha_words).lower():
        await message.answer("Капча пройдена!")
        await state.finish()
    else:
        await message.answer("Попробуйте еще раз...")

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)

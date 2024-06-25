from config import *
from kb import *

# Стартовое сообщение
@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    await message.answer('Здравствуйте, я чат-бот, который поможет Вам найти любой интересующий вас пестицид', parse_mode='HTML', reply_markup=await mainKB())

# Меню с информацией
@dp.callback_query_handler(lambda c: c.data == 'main - ℹ️ Информация')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('ПОЛЕЗНАЯ ИНФОРМАЦИЯ!!!', parse_mode='html', reply_markup = await infoKB())

# Выход из меню информация на начальное сообщение
@dp.callback_query_handler(lambda c: c.data == 'info - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await callback_query.message.edit_text('Здравствуйте, я чат-бот, который поможет Вам найти любой интересующий вас пестицид', parse_mode='HTML', reply_markup=await mainKB())

# Поиск пестицидов
@dp.callback_query_handler(lambda c: c.data == 'main - 🔍 Найти пестицид')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())



@dp.callback_query_handler(lambda c: c.data == 'pesticides - 📗 Список пестицидов')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)

    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Список пестицидов', parse_mode='html', reply_markup = await alphabetKB())

@dp.callback_query_handler(lambda c: c.data == 'pesticides - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Здравствуйте, я чат-бот, который поможет Вам найти любой интересующий вас пестицид', parse_mode='HTML', reply_markup=await mainKB())


@dp.callback_query_handler(lambda c: c.data == 'pesticidesListKB - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())

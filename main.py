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

    r = requests.get("https://www.agroxxi.ru/goshandbook/wiki/pesticides")
    html = BS(r.content, 'html.parser')

    # Список для хранения названий пестицидов
    name_pesticides = []

    # Извлечение данных
    for el in html.select(".listcatzrast > .row"):
        title = el.select('.alfabet-title > a')
        if title:
            name_pesticides.append({'name_pesticides': title[0].text})

    # Запись данных в файл JSON
    with open('name_pesticides.json', 'w', encoding='utf-8') as f:
        json.dump(name_pesticides, f, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в файл name_pesticides.json")


    # Загрузка данных из JSON файла
    with open('name_pesticides.json', 'r', encoding='utf-8') as f:
        pesticides = json.load(f)

    # Обработчик для текстовых сообщений
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def handle_text_message(message: types.Message):

        user_input = message.text.lower()
        # found_pesticide = next((p for p in pesticides if p['name_pesticides'].lower() == user_input), None)
        found_pesticide = [p for p in pesticides if user_input in p['name_pesticides'].lower()]
        
        if found_pesticide:
            # await message.reply(f'Найден пестицид: {found_pesticides["name_pesticides"]}')
            
            # response = "Найдены следующие пестициды:\n" + "\n".join([p['name_pesticides'] for p in found_pesticide])

            async def pesticides_nameKB():
                buttons = [p['name_pesticides'] for p in found_pesticide]
                btn = [InlineKeyboardButton(button, callback_data=f'pesticides - {button}')
                        for button in buttons]
                    # Создание кнопки "Назад"
                back_button = InlineKeyboardButton('Назад', callback_data='pesticides - back')
                
                btn.append(back_button)
                inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
                return inl_menu
            
            await message.answer("Найдены следующие пестициды", reply_markup=await pesticides_nameKB())

        else:
            await message.answer('Пестицид не найден. Попробуйте ввести другое название.')

                

@dp.callback_query_handler(lambda c: c.data == 'pesticides - back')
async def process_callback_pesticidesBack(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await callback_query.message.delete(callback_query.message.text)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())
    

    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Список пестицидов', parse_mode='html', reply_markup = await alphabetKB())


@dp.callback_query_handler(lambda c: c.data == 'pesticidesMenu - 📗 Список пестицидов')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)

    
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Список пестицидов', parse_mode='html', reply_markup = await alphabetKB())

@dp.callback_query_handler(lambda c: c.data == 'pesticidesMenu - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Здравствуйте, я чат-бот, который поможет Вам найти любой интересующий вас пестицид', parse_mode='HTML', reply_markup=await mainKB())


@dp.callback_query_handler(lambda c: c.data == 'pesticidesListKB - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())

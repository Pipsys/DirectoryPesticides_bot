from config import *
from kb import *
from msg_text import *

# Стартовое сообщение
@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    await message.answer(welcome_msg, parse_mode='HTML', reply_markup=await mainKB())

# Меню с информацией
@dp.callback_query_handler(lambda c: c.data == 'main - ℹ️ Информация')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(info_msg, parse_mode='html', reply_markup = await infoKB())

# Выход из меню информация на начальное сообщение
@dp.callback_query_handler(lambda c: c.data == 'info - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await callback_query.message.edit_text(welcome_msg, parse_mode='HTML', reply_markup=await mainKB())

# Поиск пестицидов
@dp.callback_query_handler(lambda c: c.data == 'main - 🔍 Найти пестицид')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())

    r = requests.get('https://www.agroxxi.ru/goshandbook/wiki/pesticides')
    html = BS(r.content, 'html.parser')

    name_pesticides = []
            
    for el in html.select(".listcatzrast > .row"):
        title = el.select('.alfabet-title a')
        if title:
            name_pesticides.append({'name_pesticides': title[0].text, 'link': title[0].get('href')})

    # Запись данных в файл JSON
    with open('json/pesticides_name.json', 'w', encoding='utf-8') as f:
        json.dump(name_pesticides, f, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в файл name_pesticides.json")

    # Загрузка данных из JSON файла
    with open('json/pesticides_name.json', 'r', encoding='utf-8') as f:
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
                # buttons = [p['name_pesticides'] for p in found_pesticide]
                buttons = [InlineKeyboardButton(p['name_pesticides'], callback_data=f'pesticide_{p["name_pesticides"]}')
                        for p in found_pesticide]
                back_button = InlineKeyboardButton('Назад', callback_data='pesticides - back')
                inl_menu = InlineKeyboardMarkup(row_width=1).add(*buttons, back_button)
                return inl_menu
            
            await message.answer("Найдены следующие пестициды", reply_markup=await pesticides_nameKB())

        else:
            await message.answer('Пестицид не найден. Попробуйте ввести другое название.')

             
@dp.callback_query_handler(lambda c: c.data.startswith('pesticide_'))
async def process_callback_pesticide(callback_query: types.CallbackQuery):
    print(callback_query.data)
        
    pesticide_name = callback_query.data[len('pesticide_'):]

    with open('json/pesticides_name.json', 'r', encoding='utf-8') as f:
        pesticides = json.load(f)

    found_pesticide = next((p for p in pesticides if p['name_pesticides'] == pesticide_name), None)

    # await callback_query.message.edit_text(f"Ссылка на {found_pesticide['name_pesticides']}: https://www.agroxxi.ru{found_pesticide['link']}")
    
    r = requests.get(f"https://www.agroxxi.ru{found_pesticide['link']}")
    html = BS(r.content, 'html.parser')

    h1_name = html.find("h1")
    h2_group = html.find(attrs={'itemprop': 'category'})

    prephar = html.find("div", class_="prephar")

    pesticide_info = {}

    paragraphs = prephar.find_all('p')

    # Обработка каждого абзаца
    for paragraph in paragraphs:
        bold_text = paragraph.find('b')
        if bold_text:
            key = bold_text.get_text(strip=True).rstrip(':')
            value = paragraph.get_text().replace(bold_text.get_text(), '').strip()
            pesticide_info[key] = value

    # Вывод информации о препарате
    # for key, value in pesticide_info.items():
    #     print(f"{key}: {value}")
    #     # await callback_query.message.answer(f"{key}: {value}", parse_mode='html')

    with open('json/pesticide_info.json', 'w', encoding='utf-8') as f:
        json.dump(pesticide_info, f, ensure_ascii=False, indent=4)

    with open('json/pesticide_info.json', 'r', encoding='utf-8') as f:
        pesticide_info = json.load(f)

    # await callback_query.message.edit_text(f"<b>{h1_name.text}</b>\n{h2_group.text}\n<b>{key}:</b> {value}", parse_mode='html')
    # message_text = f"<b>{pesticide_info.get('Название', 'Название не найдено')}</b>\n"
    message_text = f"<b>{h1_name.text}</b>\n\n{h2_group.text}\n"
    for key, value in pesticide_info.items():
        # if key != 'Название':
        #     message_text += f"\n<b>{key}:</b> {value}\n"
        message_text += f"<b>{key}:</b> {value}\n"

    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(message_text, parse_mode="html", reply_markup=await pesticide_dataKB())
    
@dp.callback_query_handler(lambda c: c.data == 'pesticidData - 📗 Список пестицидов')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Список пестицидов', parse_mode='html', reply_markup = await alphabetKB())

def load_pesticides_data():
    with open('json/pesticides_name.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    
pesticides_data = load_pesticides_data()

# async def pesticideKB(pesticides, letter):
#     btn = [InlineKeyboardButton(item['name_pesticides'], callback_data=f'pesticide - {item["link"]}') for item in pesticides]
#     back_button = InlineKeyboardButton('Назад', callback_data=f'back - {letter}')
#     btn.append(back_button)
#     inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
#     return inl_menu

async def pesticideKB(pesticides, letter, page=0, items_per_page=10):
    start = page * items_per_page
    end = start + items_per_page
    btn = [InlineKeyboardButton(item['name_pesticides'], callback_data=f'pesticidelist - {item["link"]}') for item in pesticides[start:end]]
    back_button = InlineKeyboardButton('Назад', callback_data=f'back - {letter}')

    if start > 0:
        prev_button = InlineKeyboardButton('⬅️', callback_data=f'page - {letter} - {page-1}')
        btn.append(prev_button)
    if end < len(pesticides):
        next_button = InlineKeyboardButton('➡️', callback_data=f'page - {letter} - {page+1}')
        btn.append(next_button)
    
    btn.append(back_button)
    inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
    return inl_menu

@dp.callback_query_handler(lambda c: c.data.startswith('alphabet'))
async def process_alphabet_callback(callback_query: types.CallbackQuery):
    data = callback_query.data.split(' - ')[1]
    if data == 'Назад':
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())
    else:
        # Фильтрация пестицидов по выбранной букве
        filtered_pesticides = [item for item in pesticides_data if item['name_pesticides'].startswith(data)]
        if filtered_pesticides:
            pesticides_kb = await pesticideKB(filtered_pesticides, data)
            await callback_query.message.edit_text(f'Пестициды на букву {data}:', reply_markup=pesticides_kb)
        else:
            # await bot.send_message(callback_query.from_user.id, f'Нет данных для буквы {data}')
            await bot.answer_callback_query(callback_query.id, text=f'Нет данных для буквы {data}', show_alert=False)
        await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('page'))
async def process_page_callback(callback_query: types.CallbackQuery):
    _, letter, page = callback_query.data.split(' - ')
    page = int(page)
    filtered_pesticides = [item for item in pesticides_data if item['name_pesticides'].startswith(letter)]
    pesticides_kb = await pesticideKB(filtered_pesticides, letter, page)
    await bot.edit_message_text(f'Пестициды на букву {letter}:', callback_query.from_user.id, callback_query.message.message_id, reply_markup=pesticides_kb)
    await bot.answer_callback_query(callback_query.id)
    
@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def process_back_callback(callback_query: types.CallbackQuery):
    alphabet_kb = await alphabetKB()
    await callback_query.message.edit_text("Выберите букву алфавита:", reply_markup=alphabet_kb)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('pesticidelist'))
async def process_callback_pesticide(callback_query: types.CallbackQuery):
    # try:
        print(callback_query.data)

        pesticide_name = callback_query.data[len('pesticidelist'):].strip()

        with open('json/pesticides_name.json', 'r', encoding='utf-8') as f:
            pesticides = json.load(f)

        found_pesticide = next((p for p in pesticides))
        # found_pesticide = next((p for p in pesticides if p['link'] == pesticide_name), None)
        found_pesticide = next((p for p in pesticides if p['name_pesticides'] == pesticide_name), None)

        # if found_pesticide is None:
        #     # await callback_query.message.edit_text("Пестицид не найден.")
        #     await callback_query.message.answer("Пестицид не найден")
        #     return

        r = requests.get(f"https://www.agroxxi.ru{found_pesticide['link']}")
        html = BS(r.content, 'html.parser')

        h1_name = html.find("h1")
        h2_group = html.find(attrs={'itemprop': 'category'})
        prephar = html.find("div", class_="prephar")

        if not h1_name or not h2_group or not prephar:
            await callback_query.message.edit_text("Не удалось получить информацию о пестициде.")
            return

        pesticide_info = {}
        paragraphs = prephar.find_all('p')

        for paragraph in paragraphs:
            bold_text = paragraph.find('b')
            if bold_text:
                key = bold_text.get_text(strip=True).rstrip(':')
                value = paragraph.get_text().replace(bold_text.get_text(), '').strip()
                pesticide_info[key] = value

        with open('json/pesticide_info.json', 'w', encoding='utf-8') as f:
            json.dump(pesticide_info, f, ensure_ascii=False, indent=4)

        with open('json/pesticide_info.json', 'r', encoding='utf-8') as f:
            pesticide_info = json.load(f)

        message_text = f"<b>{h1_name.text}</b>\n\n{h2_group.text}\n"
        for key, value in pesticide_info.items():
            message_text += f"<b>{key}:</b> {value}\n"

        print(callback_query.data)
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.edit_text(message_text, parse_mode="html", reply_markup=await pesticide_dataKB())

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     await callback_query.message.edit_text("Произошла ошибка при обработке запроса.")

@dp.callback_query_handler(lambda c: c.data == 'pesticidData - Прочитать подробнее')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Ссылка на пестицид')

@dp.callback_query_handler(lambda c: c.data == 'pesticidesMenu - 📗 Список пестицидов')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Список пестицидов', parse_mode='html', reply_markup = await alphabetKB())


@dp.callback_query_handler(lambda c: c.data == 'pesticidesMenu - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(welcome_msg, parse_mode='HTML', reply_markup=await mainKB())

@dp.callback_query_handler(lambda c: c.data == 'pesticidesListKB - Назад')
async def process_callback_pesticides(callback_query: types.CallbackQuery):
    print(callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Напишите назвние пестицида или используйте удобный список.\nНайдется все!', parse_mode='html', reply_markup = await pesticidesKB())

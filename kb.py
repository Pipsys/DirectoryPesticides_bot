from config import *


async def mainKB():
    buttons = ['ℹ️ Информация','🔍 Найти пестицид',]
    btn = [InlineKeyboardButton(button, callback_data=f'main - {button}')
            for button in buttons]
    inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
    return inl_menu

async def pesticidesKB():
    buttons = ['📗 Список пестицидов','Назад']
    btn = [InlineKeyboardButton(button, callback_data=f'pesticidesMenu - {button}')
            for button in buttons]
    inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
    return inl_menu

async def pesticidesListKB():
    buttons = ['Назад']
    btn = [InlineKeyboardButton(button, callback_data=f'pesticidesListKB - {button}')
            for button in buttons]
    inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
    return inl_menu

async def infoKB():
    buttons = ['Назад']
    btn = [InlineKeyboardButton(button, callback_data=f'info - {button}')
            for button in buttons]
    inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
    return inl_menu


async def alphabetKB():
        buttons = ['А','Б','В','Г','Д',
                   'Е','Ё','Ж','З','И',
                   'Й','К','Л','М','Н',
                   'О','П','Р','С','Т',
                   'У','Ф','Х','Ц','Ч',
                   'Ш','Щ','Ъ','Ы','Ь',
                   'Э','Ю','Я','Назад']
        btn = [InlineKeyboardButton(button, callback_data=f'alphabet - {button}')
                for button in buttons]
        inl_menu = InlineKeyboardMarkup(row_width=4).add(*btn)
        return inl_menu


from config import *
from main import *

async def on_startup(_):
    print('INFO: Бот в режиме онлайн')
    
if __name__ == '__main__':  
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

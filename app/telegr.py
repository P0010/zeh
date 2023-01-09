from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from app import app

API_TOKEN = app.config['API_TOKEN']  # наш токен
bot = Bot(token=API_TOKEN)  # создаём бот
dp = Dispatcher(bot)  # диспетчер

# асинхронная функция с передачей телефона и e-mail

async def somefunc(name, phone, topic):  # Принимаем три переменные из index
    text = topic +'\nИмя: ' + name + '\nТелефон: ' + phone
    await bot.send_message(-1001217772538, text)  # личный ID или ID чата

# Если нужен запуске
# if __name__ == '__main__':
#     executor.start(dp, somefunc())
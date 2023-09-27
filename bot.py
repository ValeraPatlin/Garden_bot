import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import command
import parser_text
import email_form
import logging
import os
from dotenv import load_dotenv


logger = logging.getLogger("logger_bot")

load_dotenv()

TOKEN_API = os.getenv("TOKEN_API")


# создаём бота
bot = Bot(TOKEN_API)
dispatcher = Dispatcher(bot)

# создаём клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

keyboard.add(KeyboardButton("/help"))
keyboard.insert(KeyboardButton("/website"))
keyboard.insert(KeyboardButton("/address"))
keyboard.add(KeyboardButton("/question"))
keyboard.insert(KeyboardButton("/certificate"))
keyboard.insert(KeyboardButton("/price"))
keyboard.add(KeyboardButton("/low"))
keyboard.insert(KeyboardButton("/high"))
keyboard.insert(KeyboardButton("/custom"))
keyboard.add(KeyboardButton("/lohistoryw"))


async def on_startup(_):
    logger.debug(" Start dot ")
    

@dispatcher.message_handler(commands = ["start"])
async def start_command_messege(message: types.Message):
    if not message.from_user.is_bot:    
        await bot.send_sticker(message.from_id, 
                               sticker = command.STICEKER_HELLO,
                               reply_markup = keyboard)
        
        await message.answer(text = command.START_COMMAND)
        await message.delete()
        
        email_form.send_email(message)


@dispatcher.message_handler(commands = ["help", "hh"])
async def help_command_messege(message: types.Message):
    if not message.from_user.is_bot:  
        await message.reply(text = command.HELP_COMMAND, parse_mode = "HTML")
        await message.delete()
    

@dispatcher.message_handler(commands = ["website"])
async def website_command_messege(message: types.Message):
    if not message.from_user.is_bot:  
        await message.reply(text = command.WEBSITE)
        await message.delete()


@dispatcher.message_handler(commands = ["address"])
async def address_command_message(message: types.Message):
    if not message.from_user.is_bot:
        await bot.send_location(chat_id = message.from_user.id, 
                                latitude = 59.658649, longitude = 30.119442)
        await message.delete()


@dispatcher.message_handler(commands = ["question"])
async def question_command_messege(message: types.Message):
    if not message.from_user.is_bot:  
        await message.reply(text = command.QUESTION_COMMAND)
        parser_text.quest = True
        await message.delete()
        

@dispatcher.message_handler(commands = ["certificate"])
async def certificate_command_messege(message: types.Message):
    if not message.from_user.is_bot:  
        await message.reply(text = command.CERTIFICATE_COMMAND)
        parser_text.certificate = True
        await message.delete()


@dispatcher.message_handler(commands = ["price"])
async def price_command_messege(message: types.Message):
    if not message.from_user.is_bot:  
        await message.reply(text = command.PRICE_COMMAND)
        parser_text.price = True
        await message.delete()


#  ----------------------------------------------------------------------



@dispatcher.message_handler(commands = ["low"])
async def low_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        pass
        await message.delete()


@dispatcher.message_handler(commands = ["high"])
async def high_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        pass
        await message.delete()


@dispatcher.message_handler(commands = ["custom"])
async def custom_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        pass
        await message.delete()


@dispatcher.message_handler(commands = ["history"])
async def history_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        pass
        await message.delete()






# -------------------------
#
#/low — вывод минимальных показателей (с изображением товара/услуги/и так далее);
#
#/high — вывод максимальных (с изображением товара/услуги/и так далее);
#
#/custom — вывод показателей пользовательского диапазона (с изображением товара/услуги/и так далее);
#
#/history — вывод истории запросов пользователей.







@dispatcher.message_handler()
async def user_message_text(message: types.Message):
    if not message.from_user.is_bot:  
        with open("user_text.txt", "a", encoding = "utf-8") as file:
            file.write(message.text + "\n")
            file.write(str(message.from_id))        
            file.write("\n")
            file.write(str(message.from_user))
            file.write("\n")
        
        
        
        string, sertif, price = parser_text.parser(message)
        
        await message.answer(string)
          
        if sertif:
            file = open("sertif.jpg", "rb")
            
            await bot.send_photo(chat_id = message.from_user.id,
                                 photo = file)
            
        if price:
            file = open("price.xlsx", "rb")
            
            await bot.send_document(chat_id = message.from_user.id, document = file)



def bot_start():
    executor.start_polling(dispatcher, on_startup = on_startup, skip_updates = True)
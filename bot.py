import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import command
import parser_text
import email_form
import logging
import os
from dotenv import load_dotenv
import usersDB
from datetime import datetime


logger = logging.getLogger("logger_bot")

load_dotenv()

TOKEN_API = os.getenv("TOKEN_API")


# создаём бота
bot = Bot(TOKEN_API)
dispatcher = Dispatcher(bot)

# создаём клавиатуру
keyboard_main = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

keyboard_main.add(KeyboardButton("/help"))
keyboard_main.insert(KeyboardButton("/website"))
keyboard_main.insert(KeyboardButton("/address"))
keyboard_main.add(KeyboardButton("/question"))
keyboard_main.insert(KeyboardButton("/certificate"))
keyboard_main.insert(KeyboardButton("/price"))
keyboard_main.add(KeyboardButton("/low"))
keyboard_main.insert(KeyboardButton("/high"))
keyboard_main.insert(KeyboardButton("/custom"))
keyboard_main.add(KeyboardButton("/lohistoryw"))

# создаём клавиатуру
keyboard_category = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

keyboard_category.add(KeyboardButton("/pears"))         # груши
keyboard_category.add(KeyboardButton("/apple"))         # яблони
keyboard_category.add(KeyboardButton("/cherries"))      # вишни

# создаём клавиатуру
keyboard_email = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

keyboard_email.add(KeyboardButton("/email"))
keyboard_email.add(KeyboardButton("/telegram"))



def text_messege(arr : list) -> str:
    if arr:
        string = ""
                    
        for i in arr:
            string += str(i[1]) + " \t " + str(i[2]) + "\n"
            
        return string
    
    logger.error(f"{datetime.now()}: Error: {arr=} \n")
    
    return command.ERROR_COMMAND
 


async def recording_actions_user(action : str) -> None:
    """ Запись комманд в базу данных """
    pass



async def on_startup(_):
    logger.debug(f"{datetime.now()}: Start dot ")
    
    

@dispatcher.message_handler(commands = ["start"])
async def start_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("start")
         
        await bot.send_sticker(message.from_id, 
                               sticker = command.STICEKER_HELLO,
                               reply_markup = keyboard_main)
        
        await message.answer(text = command.START_COMMAND)
        await message.delete()
        
        email_form.send_email(message)



@dispatcher.message_handler(commands = ["help", "hh"])
async def help_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("help")
        
        await message.reply(text = command.HELP_COMMAND, parse_mode = "HTML")
        await message.delete()
    


@dispatcher.message_handler(commands = ["website"])
async def website_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("website")
        
        await message.reply(text = command.WEBSITE)



@dispatcher.message_handler(commands = ["address"])
async def address_command_message(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("address")
        
        await bot.send_location(chat_id = message.from_user.id, 
                                latitude = 59.658649, longitude = 30.119442)



@dispatcher.message_handler(commands = ["email"])
async def email_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("email")
        
        await message.reply(text = command.EMAIL_COMMAND)
        



@dispatcher.message_handler(commands = ["telegram"])
async def telegram_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("telegram")
        
        if parser_text.certificate:
            parser_text.certificate = False
            
            await message.reply(text = "Вот один из сертификатов на нашу продукцию: \n")
            
            file = open("sertif.jpg", "rb")
            
            await bot.send_photo(chat_id = message.from_user.id,
                                 photo = file) 
    
        elif parser_text.price:
            parser_text.price = False
            
            await message.reply(text = "Вот прайс-лист на нашу продукцию: \n")
            
            file = open("price.xlsx", "rb")
            
            await bot.send_document(chat_id = message.from_user.id, document = file)

        await bot.send_message(message.from_id, 
                               command.NEXT_COMMAND, 
                               reply_markup = keyboard_main)
        
        


@dispatcher.message_handler(commands = ["question"])
async def question_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("question")
        
        await message.reply(text = command.QUESTION_COMMAND)
        parser_text.quest = True
        


@dispatcher.message_handler(commands = ["certificate"])
async def certificate_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("certificate")
        
        await message.reply(text = command.CERTIFICATE_COMMAND,
                            reply_markup = keyboard_email)
        parser_text.certificate = True 



@dispatcher.message_handler(commands = ["price"])
async def price_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("price")
        
        await message.reply(text = command.PRICE_COMMAND, 
                            reply_markup = keyboard_email)
        parser_text.price = True



# pears
# apple
# cherries


@dispatcher.message_handler(commands = ["pears"])
async def pears_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("pears")
        
        answer = usersDB.connect_DB_table("pears")
        
        if answer:
            sort_reqest_answer = usersDB.sort_array(answer) 
            string = text_messege(sort_reqest_answer)
            
            await message.reply(text = string, 
                                reply_markup = keyboard_main)
        else:
            await message.reply(text = command.ERROR_COMMAND,
                                reply_markup = keyboard_main)
        


# DEBUG:logger_userDB:2023-10-29 16:24:00.121870: Start connect DB appel 
# DEBUG:logger_userDB:2023-10-29 16:24:00.724060: Data: [(1, 'Анис алый', 2000), (2, 'Сахарный Мирон', 2500), (3, 'Кандиль орловский', 1900), (4, 'Брусничное', 1900)]
# ERROR:logger_userDB:2023-10-29 16:24:00.724550: Error: output_of_indicators='hign'
# ERROR:asyncio:Task exception was never retrieved       



@dispatcher.message_handler(commands = ["apple"])
async def apple_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("apple")
        
        answer = usersDB.connect_DB_table("apple")

        if answer:
            sort_reqest_answer = usersDB.sort_array(answer) 
            string = text_messege(sort_reqest_answer)

            await message.reply(text = string,
                                reply_markup = keyboard_main)
        else:
            await message.reply(text = command.ERROR_COMMAND,
                                reply_markup = keyboard_main)



@dispatcher.message_handler(commands = ["cherries"])
async def cherries_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("cherries")
        
        answer = usersDB.connect_DB_table("cherries")
        
        if answer:
            sort_reqest_answer = usersDB.sort_array(answer) 
            string = text_messege(sort_reqest_answer)
            
            await message.reply(text = string,
                                reply_markup = keyboard_main)
        else:
            await message.reply(text = command.ERROR_COMMAND,
                                reply_markup = keyboard_main)



#  ----------------------------------------------------------------------



@dispatcher.message_handler(commands = ["low"])
async def low_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("low")

        await message.reply(text = command.TAVAR_COMMAND, 
                            reply_markup = keyboard_category)
        
        usersDB.output_of_indicators = "low"

        await message.delete()



@dispatcher.message_handler(commands = ["high"])
async def high_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("high")
        
        
        await message.reply(text = command.TAVAR_COMMAND, 
                            reply_markup = keyboard_category)
        
        usersDB.output_of_indicators = "high"
        
        await message.delete()



@dispatcher.message_handler(commands = ["custom"])
async def custom_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("custom")
        
        await message.reply(text = command.TAVAR_COMMAND, 
                            reply_markup = keyboard_category)
        
        usersDB.output_of_indicators = "custom"
        
        await message.delete()



@dispatcher.message_handler(commands = ["history"])
async def history_command_messege(message: types.Message):
    if not message.from_user.is_bot:
        recording_actions_user("history")
        
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
        
        # -------------------------------------------------------------------
        # удалить
        with open("user_text.txt", "a", encoding = "utf-8") as file:
            file.write(message.text + "\n")
            file.write(str(message.from_id))        
            file.write("\n")
            file.write(str(message.from_user))
            file.write("\n")
        
        # -------------------------------------------------------------------------
        
        
        string = parser_text.parser(message)
        
        await message.answer(string, reply_markup = keyboard_main)
        
          





def bot_start():
    try:
        
        executor.start_polling(dispatcher, on_startup = on_startup, skip_updates = True)
        
    except Exception as error:
        logger.error(f"{datetime.now()}: Error: \t {error}")
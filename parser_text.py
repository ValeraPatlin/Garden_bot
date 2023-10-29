import re
import email_form
import usersDB
import logging
from datetime import datetime


logger = logging.getLogger("logger_parser")



TEXT_HELLO = ["привет", "здраствуйте", "здорово", "прив", "hello", "hi"]
TEXT_CONTACTS = ["связь", "связаться", "контакты", "телефон", "позвонить"] 

CONTACTS = """
 Вы можете связаться с нами по телефону или электронной почте:\n
 телефон: +7(921)222-33-44\n
 email:   service@pear-garden.ru
"""

TEXT_QUEST = """
 Я передал ваш вопрос. \n 
 Чем я ещё могу помочь?
"""

TEXT_NO_IS_PARSER = """
 Я вас не понимаю.
 Вы можете задать вопрос при помощи комманды /question
 Или связаться с нами по телефону или электронной почте:\n
 телефон: +7(921)222-33-44\n
 email:   service@pear-garden.ru
"""

TEXT_ANSWER_EMAIL = """
 Я отправил вам письмо.
 Если письмо не пришло проверти папку спам.\n
 Чем я ещё могу помочь?
"""

quest, certificate, price = False, False, False


def checking_list_word(list_one: list, list_two: list) -> bool:
    """
    """
    for elem in list_one:
        if elem in list_two:
            return True
        
    return False


def parser(message):
    """
    Функция для распарисвания текста от пользователя
    """
    
    if usersDB.output_of_indicators == "custom":
        req = re.compile(r"\b[0123456789]\d+")

        number_list = req.findall(message.text)
        
        return number_list
    
    
    text_is_parsed = False
    
    global quest, certificate, price
    
    string = message.text    
    arr = string.lower().split()
    
    reg = re.compile(r"[\w\.-]+@[\w\.-]+(?:\.[\w]+)+")
    email = reg.findall(string)
    
    logger.debug(f"{datetime.now()}: email: {email}")
    
    if quest:
        logger.debug(f"{datetime.now()}: quest")
        
        email_form.send_email(message, action = "quest")
        
        quest = False
        
        return TEXT_QUEST
     
    elif certificate and email:
        logger.debug(f"{datetime.now()}: certificate")
        
        email_form.send_email(message, action = "certificate", email_address = email[0]) 
        
        certificate = False
        
        return TEXT_ANSWER_EMAIL
   
    elif price and email:
        logger.debug(f"{datetime.now()}: price")
        
        email_form.send_email(message, action = "price", email_address = email[0])
        
        price = False
        
        return TEXT_ANSWER_EMAIL
        
        

    logger.debug(f"{datetime.now()}: answer")
    
    answer = ""
    
    if checking_list_word(TEXT_HELLO, arr):
        answer += f"Здраствуйте {message.from_user.first_name}."
        text_is_parsed = True
        
    if "сайт" in arr:
        answer += "\n https://pear-garden.tilda.ws \n"
        text_is_parsed = True
        
    if checking_list_word(TEXT_CONTACTS, arr):
        answer += CONTACTS
        text_is_parsed = True
        
    if not text_is_parsed:
        answer = TEXT_NO_IS_PARSER
    
    return answer






# https://pear-garden.tilda.ws

#
# {"id": 1038847449, "is_bot": false, "first_name": "Валерий", "username": "VPatlin", "language_code": "ru" }
#
# {"id": 721008417, "is_bot": false, "first_name": "Наталья", "last_name": "Полякова", "username": "polyak15", "language_code": "ru"}
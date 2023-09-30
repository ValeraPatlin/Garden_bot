from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
import logging


logger = logging.getLogger("logger_email")


load_dotenv()


def parser_message(message) -> str:
    logger.debug("parser_message")
    
    string = f"\n\nИмя: \t\t {message.first_name} \n" 
    string += f"Фамилия: \t {message.last_name} \n"
    string += f"логин: \t\t {message.username} \n"

    logger.debug(string)

    return string



def send_email(message, action : str = None, email_address: str = os.getenv("EMAIL")) -> None:
    """_summary_

    Args:
        message (_type_): _description_
    """
    
    try:
        logger.debug("Preparation email")

        sender = os.getenv("EMAIL")
        
        password = os.getenv("PASSWORD_EMAIL")  # сгенерированный пароль
    
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()
        server.login(sender, password)       
        
        msg = MIMEMultipart()
            
        msg["From"] = sender
        msg["To"] = email_address
      
        if action == "quest":
            logger.debug("quest")

            text_of_the_letter = message.text
            text_of_the_letter += parser_message(message.from_user)

            logger.debug(text_of_the_letter)
 
            msg["Subject"] = "Клиент задал вопрос"
                       
            msg.attach(MIMEText(text_of_the_letter))

            
        elif action == "certificate" or action == "price":
            logger.debug(f"action:  {action}")
            
            if action == "certificate":
                msg["Subject"] = "Сертификат на продукцию"
                
                file = "sertif.jpg"
     
            else:
                msg["Subject"] = "Прайс-лист"
                
                file = "price.xlsx"
 
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename = file)
            msg.attach(part)
      
        else:
            text_of_the_letter = "В телеграм бот зашел новый ползователь:\n"           
            text_of_the_letter += parser_message(message.from_user)

            msg["Subject"] = "Новый посетилель"
            
            msg.attach(MIMEText(text_of_the_letter))
           
           
        server.sendmail(sender, email_address, msg.as_string())
        server.quit()
        
        logger.debug("Email sent")
      
    except Exception as _error:
        logger.error(f"Error: \t {_error}")

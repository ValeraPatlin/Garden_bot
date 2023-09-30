import pymysql

import mysql.connector
import os

#from mysql.connector import connect, Error
from mysql.connector import Error

from dotenv import load_dotenv, find_dotenv
import logging


logger = logging.getLogger("logger_userDB")


load_dotenv()


try:
    logger.debug("Start connect")

    connection = mysql.connector.connect(
            host = os.getenv("IP_HOST"),
            user = os.getenv("USER"),
            passwd = os.getenv("PASSWORD_HOST")
        )


    logger.debug("Connect OK")

except Error as error:
    logger.error(f"Error:  {error}")
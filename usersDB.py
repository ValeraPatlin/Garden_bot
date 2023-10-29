import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import logging


logger = logging.getLogger("logger_userDB")


load_dotenv()


def connect_server():
    

    try:
        logger.debug("Start connect")

        connection = mysql.connector.connect(
                host=os.getenv("IP_HOST"),
                port=3306,
                user="co83188",
                password=os.getenv("PASSWORD_HOST"),
                db=os.getenv("DATABASE_NAME")
            )

        logger.debug("\n\n  Connect OK  \n\n")
        
        connection.close()

    except Error as error:
        logger.error(f"Error:  {error}")
        


def foo():
    try:
        connection = mysql.connector.connect(
                host=os.getenv("IP_HOST"),
                port=3306,
                user="co83188",
                password=os.getenv("PASSWORD_HOST"),
                db=os.getenv("DATABASE_NAME")
            )
        
        cursor = connection.cursor()

        select_all_rows = "SELECT * FROM users "
        
        cursor.execute(select_all_rows)
        
        rows = cursor.fetchall()
        
        print(rows)
            
        for i in rows:
            print(i)
            
        connection.close()
            
    except Error as error:
        logger.error(f"Error: {error}")
        
        
        
# ------------------------------------------------------------------------

output_of_indicators, number_list = None, None



def connect_DB_table(table: str) -> list:
    try:
        logger.debug(f"{datetime.now()}: Start connect DB appel ")
        
        connection = mysql.connector.connect(
                host=os.getenv("IP_HOST"),
                port=3306,
                user="co83188",
                password=os.getenv("PASSWORD_HOST"),
                db=os.getenv("DATABASE_NAME")
            )

        cursor = connection.cursor()
        select_all_rows = "SELECT * FROM " + table       
        cursor.execute(select_all_rows)        
        rows = cursor.fetchall()
        
        logger.debug(f"{datetime.now()}: Data: {rows}")

        connection.close()
        
        return rows
            
    except Error as error:
        logger.error(f"{datetime.now()}: Error: {error}")
        
        return None
        


def low_sort_array(arr: list) -> list:
    result = list()    
    elem, index = None, None

    for _ in range(len(arr)):
        num = arr[0][2]
        
        for i in arr:
            if num >= i[2]:
                num = i[2]
                elem = i
                index = arr.index(i)
                
        result.append(elem)
        arr.pop(index)
        
    logger.debug(f"{datetime.now()}: Data: {result}")    
    
    return result



def high_sort_array(arr: list) -> list:
    result = list()    
    elem, index = None, None

    for _ in range(len(arr)):
        num = arr[0][2]
        
        for i in arr:
            if num <= i[2]:
                num = i[2]
                elem = i
                index = arr.index(i)
                
        result.append(elem)
        arr.pop(index)
        
    logger.debug(f"{datetime.now()}: Data: {result}")    
    
    return result



def custom_sort_array(arr: list) -> list:
    result = list()    
    elem, index = None, None

    for _ in range(len(arr)):
        num = arr[0][2]
        
        for i in arr:
            if num >= i[2]:
                num = i[2]
                elem = i
                index = arr.index(i)
                
        result.append(elem)
        arr.pop(index)
        
    logger.debug(f"{datetime.now()}: Data: {result}")    
    
    return result



def sort_array(arr: list) -> list:
    global output_of_indicators
    global number_list
    
    if output_of_indicators == "low":
        output_of_indicators = None
        
        return low_sort_array(arr)
    
    elif output_of_indicators == "high":
        output_of_indicators = None
        
        return high_sort_array(arr)
        
    elif output_of_indicators == "custom":
        output_of_indicators = None
        
        if number_list:
            return custom_sort_array(arr)
        
        return None
    
    else:
        logger.error(f"{datetime.now()}: Error: {output_of_indicators=}")
        return None
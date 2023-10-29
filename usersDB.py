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



def custom_sort_array(arr: list, begin: int = 0, end: int = 0) -> list:
    result, custom_list = list(), list()    
    elem, index = None, None
    
    custom_list = [i for i in arr if begin <= i[2] <= end]

    for _ in range(len(custom_list)):
        num = custom_list[0][2]
        
        for i in custom_list:
            if num >= i[2]:
                num = i[2]
                elem = i
                index = custom_list.index(i)
        
        if elem:            
            result.append(elem)
            custom_list.pop(index)
        
    logger.debug(f"{datetime.now()}: Data: {result}")    
    
    return result




def foo(arr: list) ->tuple: # доделать !!!!!!
    begin, end = 0, 0    

    if len(arr) > 1:
        begin = int(arr[0])
        end = int(arr[1])

        if begin > end:
            begin, end = end, begin
         
    else:
        end = int(arr[0])
        
    return (begin, end)





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
            
            tu = foo(number_list)

            print(tu)   # туе изменить

            res = custom_sort_array(arr, tu[0], tu[1])
            
            return custom_sort_array(arr)
        
        return None
    
    else:
        logger.error(f"{datetime.now()}: Error: {output_of_indicators=}")
        return None
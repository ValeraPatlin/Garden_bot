import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import logging
import collections
import json


logger = logging.getLogger("logger_userDB")


load_dotenv()


output_of_indicators, number_list = None, None



def connect_server() -> mysql.connector:
    """
    Подключение к базе данных

    Returns:
        mysql.connector: _description_
    """

    try:
        logger.debug(f"{datetime.now()}: Start connect")

        connection = mysql.connector.connect(
                host=os.getenv("IP_HOST"),
                port=3306,
                user="co83188",
                password=os.getenv("PASSWORD_HOST"),
                db=os.getenv("DATABASE_NAME")
            )

        logger.debug(f"{datetime.now()}: Connect OK ")

        return connection

    except Error as error:
        logger.error(f"{datetime.now()}: Error: {error}")
        
        return None
        


def insert_DB_users(message) -> None:
    """
    Запись новых пользователей в базу данных

    Args:
        message (_type_): _description_
    """
    logger.debug(f"{datetime.now()}: insert DB users ")
    
    connection = connect_server()
    
    if connection:
        logger.debug(f"{datetime.now()}: Insert connect DB: users ")
        
        cursor = connection.cursor()
        
        select_all_rows = f"SELECT data_user FROM users WHERE username = '{message.username}'; "
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        
        logger.debug(f"{datetime.now()}: Data: {rows}")
        
        if not rows:
        
            data_user = {"1" : "start"}
            data = json.dumps(data_user)
                
            cursor.execute(f"INSERT INTO `users` VALUES (NULL, '{message.id}', '{datetime.now()}', '{message.first_name}', '{message.last_name}', '{message.username}', '{data}');")
            connection.commit()
                
            logger.debug(f"{datetime.now()}: Insert into users ")
        
            connection.close()
    


def convert_list_in_json(data: list, command: str) -> json:
    """
    Функция принимает list и команду добавляет

    Args:
        data (list): _description_
        command (str): _description_

    Returns:
        json: _description_
    """
    
    try:
        data_user = json.loads(data[0][0])

        if len(data_user) == 0:
            last = "0"

        else:
            [last] = collections.deque(data_user, maxlen = 1)
        
        if len(data_user) == 10:
            data_user.pop(str(int(last) - 9))

        last = str(int(last) + 1)           
        d = {last : command}
        data_user.update(d)  
        data_user = json.dumps(data_user)
        
        logger.debug(f"{datetime.now()}: Convert list in json OK ")
        
        return data_user
        

    except ValueError as error:
        logger.error(f"{datetime.now()}: Error: {error} \n Дескриализация не удалась")
        
    except KeyError as error:
        logger.error(f"{datetime.now()}: Error: {error} \n Удаление элемента из словаря не удалось")
        
    return None
            


def update_data_user(command : str, user_name: str) -> None:
    
    connection = connect_server()
    
    if connection:
        logger.debug(f"{datetime.now()}: Start connect DB: users for username: {user_name} ")
        
        cursor = connection.cursor()
        select_all_rows = f"SELECT data_user FROM users WHERE username = '{user_name}'; "
        cursor.execute(select_all_rows)
        
        rows = cursor.fetchall()
    
        logger.debug(f"{datetime.now()}: Rows: {rows}")

        if rows:
            logger.debug(f"{datetime.now()}: Update data_user {user_name} ")

            data_user = convert_list_in_json(rows, command)
            
            cursor.execute(f"UPDATE users SET data_user = '{data_user}' WHERE username = '{user_name}';")
            connection.commit()
            
        connection.close()
    


def connect_DB_table(table: str) -> list:
    
    connection = connect_server()

    if connection:
        logger.debug(f"{datetime.now()}: Start connect DB: {table} ")
        
        cursor = connection.cursor()
        
        select_all_rows = f"SELECT * FROM '{table}'; "
        cursor.execute(select_all_rows)        
        rows = cursor.fetchall()
        
        logger.debug(f"{datetime.now()}: Data: {rows}")

        connection.close()
        
        return rows
    
    else:
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



def numbers_custom(arr: list) ->tuple:
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
            number_tuples = numbers_custom(number_list)

            return custom_sort_array(arr, number_tuples[0], number_tuples[1])
        
        return None
    
    else:
        logger.error(f"{datetime.now()}: Error: {output_of_indicators=}")
        return None
    


def history_command_messege(user_name) -> str:
    logger.debug(f"{datetime.now()}: history command messege")
    
    connection = connect_server()
    
    if connection:
        logger.debug(f"{datetime.now()}: Start connect DB: users for username: {user_name} ")
        
        cursor = connection.cursor()
        select_all_rows = f"SELECT data_user FROM users WHERE username = '{user_name}'; "
        cursor.execute(select_all_rows)
        
        data = cursor.fetchall()
    
        logger.debug(f"{datetime.now()}: Rows: {data}")
        
        data_user = json.loads(data[0][0])
        
        string = ""
        num = 1
        
        for key in data_user:
            string += str(num) + " : " + str(data_user[key]) + "\n"
            num += 1
            
        return string
    
    return None


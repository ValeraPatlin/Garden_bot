import pymysql

ip = "92.53.96.245"

host = "vh338.timeweb.ru"

user = "co83188"

password = "1c2x3z4tOU"

db_name = "co83188_garden"


try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    print("\n\n !!!!!\n\n")

except Exception as error:
    print(error)


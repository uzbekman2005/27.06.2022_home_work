import pymysql.cursors
from config import *


def db_connection():
    try:
        connection = pymysql.connect(host=host, user=user, database=database, password=password,
                                 port=3306, cursorclass=pymysql.cursors.DictCursor)
        print("Connection Succed")
        return connection
    except Exception as ex:
        print(ex)

def createTable(connection):
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS movies(ID int primary key auto_increment, mov_title varchar(255) NOT NULL, " \
                  "mov_year int not null, mov_time TIME NOT NULL, mov_lang varchar(50) NOT NULL)"
            cursor.execute(sql)
        print("Table created successfully")
    except Exception as ex:
        print(ex)


def insertIntoTablefilms(connection, title, year, time, lang):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO movies (mov_title, mov_year,  mov_time, mov_lang) values(%s, %s, %s, %s)"
            cursor.execute(sql, (title, year,time, lang))
    except Exception as ex:
        print(ex)
    finally:
        connection.commit()






if __name__ == "__main__":
    connection = db_connection()
    createTable(connection)
    # insertIntoTable(connection, "Shaytanat", 1998, '2:20', "Uzbek")
    # insertIntoTable(connection, "Abdulhamidhon", 2012, '1:40', "Turk")
    # insertIntoTable(connection, "Black panther", 2009, '1:50', "English")
    # insertIntoTable(connection, "Nihol", 2019, '1:00', "Uzbek")

from config import *
import pymysql.cursors


def db_connection():
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database,
                                     port=3306, cursorclass=pymysql.cursors.DictCursor)
        print("Connection succeed")
        return connection
    except Exception as ex:
        print(ex)


def createTable(connection):
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS actors(act_id int primary key auto_increment, " \
                  "act_fname varchar(100) NOT NULL, act_lname varchar(100) NOT NULL, act_gender varchar(1) NOT NULL)"
            cursor.execute(sql)
        print("Table created")
    except Exception as ex:
        print(ex)


def insertToTableActors(connection, fname, lname, gender):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO actors (act_fname, act_lname, act_gender) values(%s, %s, %s)"

            cursor.execute(sql, (fname, lname, gender))
        print("INsertion succed")
    except Exception as ex:
        print(ex)
    finally:
        connection.commit()


def selectFromTableAll(connection, table):
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
    except Exception as ex:
        print(ex)


# if __name__ == "__main__":
#     connection = db_connection()
    # createTable(connection)
    # selectFromTable(connection, "actors")
    # insertToTable(connection, "Saida", "Rometova", 'f')
    # insertToTable(connection, "Alisher", "Uzoqob", 'm')
    # insertToTable(connection, "Adiz", "Rajabov", 'm')
    # insertToTable(connection, "Sug'diyona", "Azimova", 'f')

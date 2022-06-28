def createTable(connection):
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS casting(actor_id int not null, film_id int not null, " \
                  "role varchar(100) not null)"
            cursor.execute(sql)
            print("Table created")
    except Exception as ex:
        print(ex)


def insertIntoCasting(connection, actor_id, film_id, role):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO casting (actor_id, film_id, role) values(%s, %s, %s)"
            cursor.execute(sql, (actor_id, film_id, role))
    except Exception as ex:
        print(ex)
    finally:
        connection.commit()

def deleteFromCasting(connection, actor_id, film_id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM casting where actor_id = %s and film_id = %s"
            cursor.execute(sql, (actor_id,film_id))

    except Exception as ex:
        print(ex)
    finally:
        connection.commit()


def selectAllFromCasting(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT a.act_fname, a.act_lname, f.mov_title, c.role,f.mov_lang, f.mov_year " \
                  "FROM actors as a INNER JOIN casting as c ON c.actor_id = a.act_id " \
                  "INNER JOIN movies as f ON f.ID = c.film_id"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print(ex)


def bigDelete(connection, table, id, field):
    try:
        with connection.cursor() as cursor:
            sql = f"DELETE FROM {table} where {field} = {id}"
            cursor.execute(sql)
    except Exception as ex:
        print(ex)
    finally:
        connection.commit()




if __name__ == "__main__":
    print("hi")

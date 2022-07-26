from server.settings import SQL_BASE
import pymysql


def set_con():
    return pymysql.connect(**SQL_BASE)


con = set_con()


def execute_db(query, value=None, custom_cursor=None):
    global con
    if not con.open:
        con = set_con()

    with con.cursor(custom_cursor) as cursor:
        if value:
            cursor.execute(query, value)
        else:
            cursor.execute(query)

        data = cursor.fetchall()

    con.commit()

    return data


def execute_db_many(query, value_list, *args):
    try:
        global con
        if not con.open:
            con = set_con()

        with con.cursor() as cursor:
            if value_list:
                cursor.executemany(query, [tuple(list(args) + each) for each in value_list])
            else:
                raise
            data = cursor.fetchall()
        con.commit()
        return data
    except Exception:
        raise

import pymysql
import json
import middleware.context as context


def _get_db_connection():

    db_connect_info = context.get_db_info()

    print("Connection info = \n", json.dumps(db_connect_info, indent=2, default=str))

    db_connection = pymysql.connect(**db_connect_info)
    return db_connection


def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_resource(db_schema, table_name):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res

def get_resource_by_id(db_schema, table_name, id):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + table_name + "ID = " + id
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_resource_by_user(db_schema, table_name1, table_name2, resourceid):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name2 + \
          " where " + table_name2 + "ID = (select " + table_name2 + "ID from " + db_schema + "." + table_name1 + \
          " where " + table_name1 + "ID = " + resourceid + ")"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res



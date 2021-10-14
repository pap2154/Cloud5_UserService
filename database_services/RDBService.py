import pymysql
import json
import middleware.context as context

import pymysql
import json
import logging
import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:

    def __init__(self):
        pass

    @classmethod
    def _get_db_connection(cls):

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()

        db_connection = pymysql.connect(
            **db_info,
            autocommit=True
        )
        return db_connection

    @classmethod
    def get_full_resource(cls, db_schema, table_name):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()
        return res

    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False):

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            res = None
            conn.close()
            print(e)
            raise e

        return res

    @classmethod
    def get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " + " AND ".join(terms)

        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template):

        wc, args = RDBService.get_where_clause_args(template)

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " " + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
            column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_resource(cls, db_schema, table_name):

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def update(cls, db_schema, table_name, update_data, id):

        cols = []
        args = []

        for k, v in update_data.items():
            cols.append(k)
            args.append(v)

        sql_stmt = "update " + db_schema + "." + table_name + " set "
        for i in range(len(cols)):
            sql_stmt += cols[i] + "=%s"
            if i != len(cols)-1:
                sql_stmt += ", "
        sql_stmt += " where " + table_name + "ID = " + id

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def delete_resource(cls, db_schema, table_name, id):

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "delete from " + db_schema + "." + table_name + " where " + table_name + "ID = " + id
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)

        conn.close()

        return res

    @classmethod
    def delete_history_by_userID_movieID(cls, db_schema, table_name, userID, movieID):

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "delete from " + db_schema + "." + table_name + " where userID = " + userID + " and movieID = " + movieID
        print("SQL Statement = " + cur.mogrify(sql, None))
        res = cur.execute(sql)

        conn.close()

        return res

    @classmethod
    def get_resource_by_column_id(cls, db_schema, table_name, column, id):

        conn = cls._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + column + " = " + id
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    # @classmethod
    # def get_resource_by_id(cls, db_schema, table_name, id):
    #
    #     conn = cls._get_db_connection()
    #     cur = conn.cursor()
    #
    #     sql = "select * from " + db_schema + "." + table_name + " where " + table_name + "ID = " + id
    #     print("SQL Statement = " + cur.mogrify(sql, None))
    #
    #     res = cur.execute(sql)
    #     res = cur.fetchall()
    #
    #     conn.close()
    #
    #     return res

    # @classmethod
    # def get_resource_by_user(cls, db_schema, table_name1, table_name2, resourceid):
    #
    #     conn = cls._get_db_connection()
    #     cur = conn.cursor()
    #
    #     sql = "select * from " + db_schema + "." + table_name2 + \
    #           " where " + table_name2 + "ID = (select " + table_name2 + "ID from " + db_schema + "." + table_name1 + \
    #           " where " + table_name1 + "ID = " + resourceid + ")"
    #     print("SQL Statement = " + cur.mogrify(sql, None))
    #
    #     res = cur.execute(sql)
    #     res = cur.fetchall()
    #
    #     conn.close()
    #
    #     return res


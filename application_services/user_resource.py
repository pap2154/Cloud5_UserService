from application_services.BaseApplicationResource import BaseApplicationResource
from database_services.RDBService import RDBService


class userResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()


    #resource_data is a dictionary of the information that we want to turn into a link array
    @classmethod
    def get_links(cls, resource_data):
        for r in resource_data:
            address_id = r.get('addressID')
            user_id = r.get('userID')

            links = []
            self_link = {"rel": "self", "href": "/users/" + str(user_id)}
            links.append(self_link)

            if address_id:
                address_link = {"rel": "address", "href": "/addresses/" + str(address_id)}
                links.append(address_link)

            r["links"] = links
        return resource_data

    @classmethod
    def get_all_users(cls):
        return RDBService.get_resource("user_service", "user")

    @classmethod
    def get_user_by_id(cls, id):
        return RDBService.find_by_template("user_service", "user",
                                           {"userID": id})
    @classmethod
    def get_address_by_user(cls, db_schema, table_name1, table_name2, resourceid):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name2 + \
              " where " + table_name2 + "ID = (select " + table_name2 + "ID from " + db_schema + "." + table_name1 + \
              " where " + table_name1 + "ID = " + resourceid + ")"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def add_user(cls, user):
        return RDBService.create("user_service", "user", user)

    @classmethod
    def update_user(cls, id, update_data):
        return RDBService.update("user_service", "user", update_data, id)

    @classmethod
    def delete_user(cls, id):
        return RDBService.delete_resource("user_service", "user", id)

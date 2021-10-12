from application_services.BaseApplicationResource import BaseApplicationResource
from database_services.RDBService import RDBService


class addressResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_all_addresses(cls):
        return RDBService.get_resource("user_service", "address")

    @classmethod
    def get_address_by_id(cls, id):
        return RDBService.find_by_template("user_service", "address",
                                           {"addressID": id})

    @classmethod
    def get_user_by_address(cls, id):
        return RDBService.find_by_template("user_service", "user",
                                           {'addressID': id})

    @classmethod
    def add_address(cls, address):
        return RDBService.create("user_service", "address", address)

    @classmethod
    def update_address(cls, id, update_data):
        return RDBService.update("user_service", "address", update_data, id)

    @classmethod
    def delete_address(cls, id):
        return RDBService.delete_resource("user_service", "address", id)
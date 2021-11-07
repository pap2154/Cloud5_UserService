from application_services.BaseApplicationResource import BaseApplicationResource
from database_services.RDBService import RDBService


class movieHistoryResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        for r in resource_data:
            movie_id = r.get('movieID')
            user_id = r.get('userID')

            links = []
            if user_id:
                user_link = {"rel": "user", "href": "/users/" + str(user_id)}
                links.append(user_link)

#how do I get movie information which is in a different service

            # if movie_id:
            #     address_link = {"rel": "movies", "href": "/movies/" + str(address_id)}
            #     links.append(address_link)

            r["links"] = links
        return resource_data

    @classmethod
    def get_all_history(cls):
        return RDBService.get_resource("user_service", "userMovieHistory")

    @classmethod
    def add_history(cls, history):
        return RDBService.create("user_service", "userMovieHistory", history)

    @classmethod
    def get_history_by_user_id(cls, id):
        return RDBService.get_resource_by_column_id("user_service", "userMovieHistory", "userID", id)

    @classmethod
    def get_history_by_movie_id(cls, id):
        return RDBService.get_resource_by_column_id("user_service", "userMovieHistory", "movieID", id)

    @classmethod
    def get_liked_movies(cls, id):
        return RDBService.find_by_template("user_service", "userMovieHistory", {"userID": id, "likedMovie": 1})

    @classmethod
    def get_disliked_movies(cls, id):
        return RDBService.find_by_template("user_service", "userMovieHistory", {"userID": id, "likedMovie": 0})

    @classmethod
    def get_history_by_user_movie_id(cls, userID, movieID):
        return RDBService.find_by_template("user_service", "userMovieHistory", {"userID": userID, "movieID": movieID})

    @classmethod
    def delete_history_by_user_movie_id(cls, userID, movieID):
        return RDBService.delete_history_by_userID_movieID("user_service", "userMovieHistory", userID, movieID)

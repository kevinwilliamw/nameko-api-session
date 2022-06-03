import dependencies

from nameko.rpc import rpc

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def add_user(self, username, password):
        user = self.database.add_user(username, password)
        return user

    @rpc
    def get_user(self, username, password):
        user = self.database.get_user(username, password)
        return user
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from model.User import User
from controller.Register import Register


class UserManagement:

    def __init__(self, **kw):
        super().__init__( **kw )

        self.__users = []
        self.account_data()

    def add_user(self, login, password):
        if login == "" or password == "":
            return "error"

        else:
            if not self.search_user(login):
                self.__users.append( User( login, password ) )

                return True
            else:
                return "user_exists"


    def search_user(self, login):
        for i in range( len( self.__users ) ):
            if login == self.__users[i].login:
                return self.__users[i].login

        return False



    def search_password(self, login, password):
        for user in self.__users:
            if login == user.login:
                if password == user.password:


                    return True

        return False


    def remove_user(self):
        pass

    def account_data(self):

        self.__users.append( User( "Feef", "321" ) )
        self.__users.append( User( "Felix", "321" ) )
        self.__users.append( User( "Pao", "123" ) )
        self.__users.append( User( "Teste", "444" ) )
        self.__users.append( User( "1", "1" ) )

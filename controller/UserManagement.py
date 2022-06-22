from model.User import User
import time


class UserManagement:
    def __init__(self, **kw):
        super().__init__( **kw )
        self.__users_dict = {}
        self.__current_user = None
        self.account_data()

    def add_user(self, new_user_data):
        try:
            if self.__users_dict[new_user_data["login"]]:
                return False
        except KeyError:
            self.__users_dict[new_user_data["login"]] = User(new_user_data)
            return True

    def search_user(self, login_data):
        # Try to acess user by login (unique key) and verify if password matches.
        try:
            if self.__users_dict[login_data["login"]].user_data["pwd"] == login_data["pwd"]:
                # If do, set current_user and return True to approve login.
                self.__current_user = self.__users_dict[login_data["login"]]
                return True
        except KeyError:
            # If not, just return False.
            return False

    def remove_user(self):
        pass

    def update_user_personal_configs(self, dict_data):
        for key, value in dict_data.items():
            self.__current_user.personal_configs[key] = value

        # Get current user login
        current_login = self.__current_user.user_data["login"]

        # Search for user in dicts by current user login and set new value.
        self.__users_dict[current_login].personal_configs = self.__current_user.personal_configs

    def update_user_data(self, dict_data):
        for key, value in dict_data.items():
            self.__current_user.user_data[key] = value

            # Get current user login
            current_login = self.__current_user.user_data["login"]

            # Search for user in dicts by current user login and set new value.
            self.__users_dict[current_login].user_data = self.__current_user.user_data

    def get_user_data(self, data):
        if type(data) == str:
            return self.__current_user.user_data[data]
        elif type(data) == dict:
            for key, values in data.items():
                return self.__current_user.user_data[key][values]

    @property
    def current_user(self):
        return self.__current_user

    @current_user.setter
    def current_user(self, current_user):
        self.__current_user = current_user


    # For tests only.
    def account_data(self):
        self.__users_dict["Feef"] = User({"name": "Feef", "last_name": "", "login": "Feef", "email": "peppepjanj",
                                          "pwd": "321", "type": 0, "first_login": True, 'current_tab': None})
        self.__users_dict["Felix"] = User({"name": "Felix", "last_name": "", "login": "Felix", "email": "peppepjanj",
                                           "pwd": "321", "type": 0, "first_login": True, 'current_tab': None})
        self.__users_dict["1"] = User({"name": "Sussi", "last_name": "", "login": "1", "email": "peppepjanj",
                                       "pwd": "1", "type": 0, "first_login": True, 'current_tab': None})
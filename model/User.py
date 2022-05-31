
class User:

    def __init__(self, dict_create):
        # Save user data in a dict. Key explanation:
        # > name: User name.
        # > last_name: Last name of user.
        # > login: User ID used to acess his account
        # > email: User email used to recover his account.
        # > pwd: User password.
        # > type: Used to define which acess level (modules) user have.
        # > first_login: Check if all confgis are already loaded in that user.
        self.__user_data = dict_create
        # Add key personal_configs in dict. It's used to define what configuration user want.
        self.__user_data["personal_configs"] = {"Font Size": 15, "Font": "Arial", "Scatter": False,
                                                "Current Tab": None}

    @property
    def user_data(self):
        return self.__user_data

    @user_data.setter
    def user_data(self, user_data):
        self.__user_data = user_data

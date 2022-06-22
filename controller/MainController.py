from kivy.properties import NumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager

# from kivy.uix.textinput import TextInput
from controller.DocsManager import DocsManager
from controller.UserManagement import UserManagement

from vision.Login import Login
from controller.Register import Register
from controller.UserMain import UserMain


class WindowManager(ScreenManager):
    Builder.load_file( "Kivy_Files/windowmanager.kv" )
    perspective_point_x = NumericProperty()
    perspective_point_y = NumericProperty()

    # Init class and create managers.
    def __init__(self, **kwargs):
        super( WindowManager, self ).__init__(**kwargs)
        self.__user_manager = UserManagement()
        self.__docs_manager = DocsManager()

    # Call functions section: used to execute functions from other classes.
    '''**********************************************************************************'''
    def call_create_doc_buttons(self):
        for widget in self.walk():
            if str(type(widget)) == "<class 'controller.TabDocs.AccordionArea'>":
                widget.create_itens(self.__docs_manager.doc_names, self.__docs_manager.pdf_dict)
                break

    def call_search_user(self, login_data):
        # Send login/pwd to UserManager
        if self.__user_manager.search_user(login_data):
            self.change_screen("Login", "UserMain")
            self.set_config_values()
            return True
        else:
            return False

    def call_start_config_values(self, user_data, user_config):
        for widget in self.walk():
            if str( type( widget ) ) == "<class 'controller.TabConfigs.TabConfigs'>":
                widget.start_config_values(user_data, user_config)
                break

    def call_update_configs(self, user_data, user_configs):
        # Send dict changed values to update user in user_manager.
        self.__user_manager.update_user_data(user_data)
        self.__user_manager.update_user_personal_configs(user_configs)

    def call_create_pdfs(self):
        user = self.__user_manager.current_user
        self.__docs_manager.check_user_signature(user.user_data)

    def call_add_user(self, new_user_data):
        return self.__user_manager.add_user(new_user_data)
    '''**********************************************************************************'''

    # Loaders section: functions used to load objects and a bunch of configurations.
    '''**********************************************************************************'''
    def get_user_personal_configs(self):
        # if self.__user_manager.get_user_data( {"personal_configs": "current_tab"} ) is not None:
        #    widget.switch_to( widget.configs )
        user_data = self.__user_manager.current_user.user_data
        user_config = self.__user_manager.current_user.personal_configs
        return user_data, user_config
    '''**********************************************************************************'''

    # Used for tests only
    '''**********************************************************************************'''
    def on_size(self, *args):
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height * 0.75

    def change_screen(self, current_screen, next_screen):
        if current_screen == "Login":
            if next_screen == "UserMain":
                self.current = "UserMain"
            elif next_screen == "Register":
                self.current = "Register"

        elif current_screen == "UserMain":
            if next_screen == "Login":
                self.current = "Login"

        elif current_screen == "Register":
            if next_screen == "Login":
                self.current = "Login"
    '''**********************************************************************************'''

    def set_config_values(self):
        if self.__user_manager.get_user_data( "first_login" ):
            # Set first login to false.
            self.__user_manager.update_user_data( {"first_login": False} )

            # Create docs based on user
            self.call_create_pdfs()
            self.call_create_doc_buttons()

            # Get current user personal configs
        user_data, user_configs = self.get_user_personal_configs()
        self.call_start_config_values( user_data, user_configs )

    # Deslog from current user.
    def deslog(self):
        self.change_screen( "UserMain", "Login" )
        self.__user_manager.current_user = None


class MainController(App):
    Config.set( 'input', 'mouse', 'mouse,multitouch_on_demand' )
    Config.set( 'kivy', 'exit_on_escape', '0' )
    Config.set( 'graphics', 'width', 1280 )
    Config.set( 'graphics', 'height', 960 )

    def build(self):
        self.title = "Doc Lawyer"
        self.icon = "imgs/main_icon.jpg"
        return WindowManager()


if __name__ == '__main__':
    MainController().run()

from kivy.properties import NumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager

from controller.DocsManager import DocsManager
from controller.UserManagement import UserManagement
from vision.Login import Login

from controller.Register import Register
from controller.UserMain import UserMain


class WindowManager(ScreenManager):
    Builder.load_file( "Kivy_Files/windowmanager.kv" )
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    width: 1280
    height: 960
    Config.set( 'graphics', 'width', 1280 )
    Config.set( 'graphics', 'height', 960 )

    def __init__(self, **kwargs):
        super( WindowManager, self ).__init__(**kwargs)
        self.__user_manager = UserManagement()
        self.__docs_manager = DocsManager()

    def user_docs(self):
        user = self.__user_manager.current_user
        self.__docs_manager.create_documents(user)
        self.__docs_manager.load_pdf(user)

    def call_create_itens(self):
        for widget in self.walk():
            if str(type(widget)) == "<class 'controller.TabDocs.AccordionArea'>":
                widget.create_itens(self.__docs_manager.doc_names, self.__docs_manager.pdf_dict)
                break

    def call_search_user(self, login_data):
        # Send login/pwd to UserManager
        if self.__user_manager.search_user(login_data):
            self.change_screen("Login", "UserMain")
            if self.__user_manager.get_user_data("first_login"):
                # Set first login to false.
                self.__user_manager.update_user( {"first_login": False} )

                # Create docs based on user
                self.user_docs()
                self.call_create_itens()

            # Load current user personal configs
            self.load_user_personal_configs()
            return True
        else:
            return False

    def call_add_user(self, new_user_data):
        return self.__user_manager.add_user(new_user_data)

    def load_user_personal_configs(self):
        for widget in self.walk():
            if str( type( widget ) ) == "<class 'controller.UserMain.Tab'>":
                if self.__user_manager.get_user_data({"personal_configs": "Current Tab"}) is not None:
                    widget.switch_to( widget.configs )

            if str( type( widget ) ) == "<class 'controller.TabConfigs.TabConfigs'>":
                widget.start_config_values( self.__user_manager.current_user.user_data)
                break

    def update_configs(self, config_values):
        # Send dict changed values to update user in user_manager.
        self.__user_manager.update_user({"personal_configs": config_values})

    def on_size(self, *args):
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height * 0.75

    def deslog(self):
        self.change_screen( "UserMain", "Login" )
        self.__user_manager.current_user = None

    # Used for tests only
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


class MainController(App):
    Config.set( 'input', 'mouse', 'mouse,multitouch_on_demand' )
    Config.set( 'kivy', 'exit_on_escape', '0' )

    def build(self):
        return WindowManager()


if __name__ == '__main__':
    MainController().run()

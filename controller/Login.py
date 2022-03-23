from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from controller.UserManagement import UserManagement

default_fields = ["Digite o login", "Digite a senha"]
class Login(Screen):
    Builder.load_file("login.kv")

    def __init__(self, **kw):
        super().__init__( **kw )
        self.__mng = UserManagement()


    def submit_login(self, login, password):
        if self.__mng.search_password(login, password):
            self.manager.current = "UserMain"

            self.parent.user_docs(login)
            self.parent.call_create_buttons()
            #print(self.children[0].ids)
        else:
            self.ids.wrong_input.text = "Usuário ou senha incorretos!"

    def verify_accounts(self, login, password):

        for x in self.account_data():

            if login == x and password != "":
                return True

            else:
                return False

    def clean(self):

        self.ids.input_login.focus = False
        self.ids.input_password.focus = False

        self.ids.input_login.text = "Digite o login"
        self.ids.input_password.text = "Digite a senha"
        self.ids.input_password.password = False
        self.ids.wrong_input.text = ""

    def login_desclick(self, text_input):

        if text_input == 1:
            if self.ids.input_login.text == "":
                self.ids.input_login.text = "Digite o login"
            elif self.ids.input_login.text == "Digite o login":
                self.ids.input_login.text = ""
        elif text_input == 2:
            self.ids.input_password.password = True
            if self.ids.input_password.text == "":
                self.ids.input_password.password = False
                self.ids.input_password.text = "Digite a senha"
            elif self.ids.input_password.text == "Digite a senha":
                self.ids.input_password.text = ""


    def register (self):
        self.manager.current = 'Register'
        self.clean()
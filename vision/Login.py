from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class Login(Screen):
    Builder.load_file( "../controller/Kivy_Files/login.kv" )

    def __init__(self, **kw):
        super().__init__( **kw )
        self.__mask_values = {535.0: "Digite o login", 475.0: "Digite a senha"}

    def submit_login(self, login, password):
        if not self.manager.call_search_user({"login": login, "pwd": password}):
            self.ids.wrong_input.text = "Usuário ou senha incorretos!"

    def clean(self):
        count = 0
        for child in self.walk():
            if str(type(child)) == "<class 'kivy.factory.LoginTextInput'>":
                child.text = ""
                self.check_data(child)
                count += 1
                if count == 2:
                    break

    def check_data(self, widget):
        if widget.focus:
            if self.__mask_values[widget.pos[1]] == widget.text:
                widget.text = ""
            if widget.pos[1] == 475.0:
                widget.password = True

        else:
            if widget.text == "":
                widget.text = self.__mask_values[widget.pos[1]]
                widget.password = False

    def register(self):
        self.manager.change_screen("Login", "Register")
        self.clean()

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import controller.UserManagement


class Register(Screen):
    def __init__(self, **kw):
        super().__init__( **kw )
        self.user_manager = controller.UserManagement.UserManagement()
    Builder.load_file("register.kv")

    def add_user(self):
        login = ''
        pwd = ''
        option = self.user_manager.add_user(login, pwd)  # return a String

        if option == "error":
            self.ids.empty_input_message.text = 'Preencha todos os campos'

        elif option == "user_exists":
            self.ids.empty_input_message.text = 'Usuário já cadastrado!'
        else:
            self.ids.empty_input_message.text = 'Registro:'
            self.ids.input_register_user.text = ''
            self.ids.input_register_pass.text = ''

            self.manager.current = 'Login'


    def testa(self, campo):
        for id in self.ids:
            print(id)


    def create(self):0
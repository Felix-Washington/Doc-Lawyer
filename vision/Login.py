from functools import partial

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class Login(Screen):
    Builder.load_file( "../controller/Kivy_Files/login.kv" )

    def __init__(self, **kw):
        super().__init__( **kw )
        self.__mask_values = {535.0: "Digite o login", 475.0: "Digite a senha"}
        self.get_current_widget_pos()

    def get_current_widget_pos(self):
        for i in self.walk():
            print(i)

    def submit_login(self, login, password):

        if not self.manager.call_search_user({"login": login, "pwd": password}):
            self.ids.wrong_input.text = "Usuário ou senha incorretos!"
            self.ids.label_feedback.opacity = 1
            Clock.schedule_once(partial(self.set_fade_on_label, self.ids.wrong_input), 3 )
            print(self.ids.wrong_input.text)

    def set_fade_on_label(self, label, *args):
        label.opacity = 1
        anim = Animation(opacity=0, duration= 3)
        anim.start(label)

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
        print(widget.pos)
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

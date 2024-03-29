from functools import partial

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class Register(Screen):
    def __init__(self, **kw):
        super().__init__( **kw )
        Builder.load_file("Kivy_Files/register.kv")

    def return_to_manager(self, new_user_data):
        correct_new_user_data = {"name": "", "last_name": "", "login": "", "email": "",
                                 "pwd": "321", "type": 0, "first_login": True}

        for key, value in new_user_data.items():
            if key == 330:
                correct_new_user_data["name"] = value
            elif key == 275:
                correct_new_user_data["last_name"] = value
            elif key == 220:
                correct_new_user_data["login"] = value
            elif key == 165:
                correct_new_user_data["email"] = value
            elif key == 110:
                correct_new_user_data["pwd"] = value

        if self.manager.call_add_user(correct_new_user_data):
            self.back_to_login_screen()
        else:
            print("user already exists")

    def get_data(self):
        for child in self.walk():
            if str(type(child)) == "<class 'controller.Register.Box_texts'>":
                condition, data = child.verify_data()

                if condition:
                    self.return_to_manager(data)
                else:
                    self.ids.label_feedback.opacity = 1
                    self.ids.label_register_feedback.text = "Preencha os campos obrigatórios"
                    Clock.schedule_once( partial( self.set_fade_on_label, self.ids.label_register_feedback ), 3 )
                break

    def set_fade_on_label(self, label, *args):
        anim = Animation(opacity=0, duration= 3)
        anim.start(label)


    def back_to_login_screen(self):
        for child in self.walk():
            if str( type( child ) ) == "<class 'controller.Register.Box_texts'>":
                child.reset_values()
                self.manager.change_screen( "Register", "Login" )
                break


class CustomRegisterButton(ButtonBehavior, Label):
    color = ListProperty([1, 0, 0, 1])
    color_pressed = ListProperty([0.1, 0.1, 0.1, 1])

    def __int__(self, **kwargs):
        super(CustomRegisterButton, self).__init__(**kwargs)
        self.update()

    def on_pos(self, *args):
        self.update()

    def on_size(self, *args):
        self.update()

    def on_press(self, *args):
        self.color, self.color_pressed = self.color_pressed, self.color

    def on_release(self, *args):
        self.color, self.color_pressed = self.color_pressed, self.color

    def on_color(self, *args):
        self.update()

    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.color, g=1)
            Ellipse( size=(self.height, self.height), pos=self.pos )
            Ellipse( size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y) )
            Rectangle( size=(self.width - self.height, self.height), pos=(self.x + self.height / 2, self.y) )


class Box_texts(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.orientation = "vertical"
        self.size_hint = None, None
        self.spacing = 5
        self.height_child = 50 + self.spacing
        self.__mask_values = {self.height_child * 6: "Nome", self.height_child * 5: "Último Nome",
                              self.height_child * 4: "Nome do Usuário", self.height_child * 3: "Email",
                              self.height_child * 2: "Senha", self.height_child * 1: "Confirme a Senha"}

        self.__data_values = {self.height_child * 6: "Nome", self.height_child * 5: "Último Nome",
                              self.height_child * 4: "Nome do Usuário", self.height_child * 3: "Email",
                              self.height_child * 2: "Senha", self.height_child * 1: "Confirme a Senha"}

        self.__required_values = {}

    def get_data(self, widget, widget_pos):
        if widget.focus:
            if self.__mask_values[widget_pos] == widget.text:
                widget.text = ""
        else:
            if widget.text == "":
                widget.text = self.__mask_values[widget_pos]
            self.__data_values[widget_pos] = widget.text

    def verify_data(self):
        for key, value in self.__mask_values.items():
            if self.__data_values[key] == value:
                return False, self.__data_values[key]
        return True, self.__data_values

    def reset_values(self):
        for child in self.walk():

            if str(type(child)) == "<class 'kivy.factory.RegisterTextInput'>":
                widget_pos_corrected = child.pos[1] - self.pos[1] + self.height_child
                child.text = self.__mask_values[widget_pos_corrected]
                self.__data_values[widget_pos_corrected] = child.text

    @property
    def data_values(self):
        return self.__data_values

    @data_values.setter
    def data_values(self, data_values):
        self.__data_values = data_values

    @property
    def mask_values(self):
        return self.__mask_values

    @mask_values.setter
    def mask_values(self, mask_values):
        self.__mask_values = mask_values


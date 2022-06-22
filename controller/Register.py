from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
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
                    for child_two in child.parent.children:
                        if str(type(child_two)) == "<class 'kivy.uix.label.Label'>":
                            child_two.text = "Campos obrigatorios"
                            break
                break

    def back_to_login_screen(self):
        for child in self.walk():
            if str( type( child ) ) == "<class 'controller.Register.Box_texts'>":
                child.reset_values()
                self.manager.change_screen( "Register", "Login" )
                break


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


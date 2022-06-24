from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial

from kivy.graphics import Ellipse, Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelItem


class TabConfigs(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(TabbedPanelItem, self).__init__( **kwargs )
        Builder.load_file( "Kivy_Files/tab_configs.kv" )
        self.text = "Configs"
        self.tab_width = 40
        self.__default_config_values = {"font_size": 15, "Font": "Times", "Scatter": True,
                                'current_tab': "<class 'controller.TabConfigs.TabConfigs'>"}
        self._popup = None

    def start_config_values(self, user_data, user_personal_configs):
        self.ids.user_data_box.set_labels(user_data)
        self.ids.s1.value = user_personal_configs["font_size"]
        self.ids.switch_scatter.active = user_personal_configs['Scatter']

    def update_to_user(self, user_data, user_configs):
        self.parent.parent.parent.parent.parent.parent.manager.call_update_configs(user_data, user_configs)

    def save(self):
        # Acess user main
        new_user_data, user_personal_configs = {}, {}
        self.ids.label_feedback.opacity = 1
        if self.ids.text_input_box.check_required_fields():
            new_user_data = self.ids.text_input_box.child_pos
            font_size = self.ids.s1.value
            scatter = self.ids.switch_scatter.active
            user_personal_configs = {"font_size": font_size, "scatter": scatter}
            self.ids.label_feedback.text = "Configurações atualizadas."

        else:
            self.ids.label_feedback.text = "Preencha os campos obrigatórios"

        Clock.schedule_once( partial( self.set_opacity_on_label, self.ids.label_feedback ), 3 )
        self.update_to_user(new_user_data, user_personal_configs)

    def set_default_configs(self, change):
        if change:
            self.ids.s1.value = self.__default_config_values['font_size']
            self.ids.switch_scatter.active = self.__default_config_values['Scatter']
            self.ids.label_feedback.text = "Configurações restauradas para padrão."
            self.ids.label_feedback.opacity = 1
            Clock.schedule_once( partial(self.set_opacity_on_label, self.ids.label_feedback), 3 )

        self._popup.dismiss()

    def set_opacity_on_label(self, label, *args):
        label.opacity = 1
        anim = Animation(opacity=0, duration= 3)
        anim.start(label)

    def create_popup_save(self):
        content = ConfirmConfigs(set_default_configs=self.set_default_configs)
        self._popup = Popup( title='Deseja alterar para os valores padrão?', content=content,
                             size_hint=(None, None), size=(200, 200), pos=(100, 100), auto_dismiss=False)
        self._popup.open()

class UserDataBox (BoxLayout):
    def __int__(self, **kwargs):
        super().__init__(**kwargs)

    def set_labels(self, user_data):
        labels = {0: "login", 1: "name", 2: "last_name", 3: "email", 4: "pwd"}
        self.children[0].start_configs(user_data, labels)


class TextInputBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.orientation = 'vertical'
        self.size_hint = None, None
        self.spacing = 5

        self.__required_fields = {1: "name", 3: "email", 4: "pwd"}
        self.__required_fields_check = {1: False, 3: False, 4: False}
        self.child_pos = {}
        self.enumerate_child_pos = {}

    def start_configs(self, user_configs, labels):
        # Assign texts for TextInput.
        for key, child in enumerate(reversed(self.children)):
            child.text = user_configs[labels[key]]
            self.child_pos[child.pos[1]] = user_configs[labels[key]]
            # Puts required field in red color.

            # Link child position with label fields.
            self.enumerate_child_pos[list(self.child_pos)[key]] = key
            try:
                if self.__required_fields[key]:
                    child.background_color = 'e79898'
                    if user_configs[labels[key]] == "":
                        self.__required_fields_check[key] = False
                    else:
                        self.__required_fields_check[key] = True
            except KeyError:
                pass

    # Get new user data and store in self.child_pos dict.
    def get_new_user_data(self, widget):
        if not widget.focus:
            if widget.text == "":
                try:
                    if self.__required_fields[self.enumerate_child_pos[widget.pos[1]]]:
                        self.__required_fields_check[self.enumerate_child_pos[widget.pos[1]]] = False
                except KeyError:
                    pass
            else:
                self.__required_fields_check[self.enumerate_child_pos[widget.pos[1]]] = True
            self.child_pos[widget.pos[1]] = widget.text

    def check_required_fields(self):
        check = False
        for value in self.__required_fields_check.values():
            if value:
                check = True
            else:
                check = False
                break

        return check


class BoxLabel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.size_hint = None, None
        self.orientation = "vertical"
        self.labels = {0: "Login", 1: "Nome", 2: "Último Nome", 3: "Email", 4: "Senha"}
        self.spacing = 5
        self.create_labels()

    def create_labels(self):
        for i in self.labels.keys():
            label = Label(text=self.labels[i])
            self.add_widget(label)

    def print_size(self):
        for i in self.children:
            print(i.size, i.pos, i.text)


class ConfirmConfigs(FloatLayout):
    set_default_configs = ObjectProperty()


class PopUpCustomButton(ButtonBehavior, Label):
    color = ListProperty([0.1, 0.5, 0.7, 1])
    color_pressed = ListProperty([0.1, 0, 0, 1])

    def __int__(self, **kwargs):
        super(PopUpCustomButton, self).__init__(**kwargs)
        self.size_hint = None, None
        self.font_size = 16
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
            Color( rgba=self.color)
            Ellipse( size=(self.height, self.height), pos=self.pos )
            Ellipse( size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y) )
            Rectangle( size=(self.width - self.height, self.height), pos=(self.x + self.height / 2, self.y) )

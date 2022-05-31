from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
#from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelItem


class TabConfigs(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        Builder.load_file( "Kivy_Files/tab_configs.kv" )
        self.text = "Configs"
        self.__config_values = {"Font Size": 15, "Font": "Times", "Scatter": True, 'Current Tab': None}
        self._popup = None
        #self.__mask_values = {self.height_child * 6: "Nome", self.height_child * 5: "Último Nome",
        #                      self.height_child * 4: "Nome do Usuário", self.height_child * 3: "Email",
        #                      self.height_child * 2: "Senha", self.height_child * 1: "Confirme a Senha"}

    def update_to_user(self, config_type, config_value):
        for widget in self.walk_reverse():
            if str(type(widget)) == "<class 'controller.UserMain.UserMain'>":
                self.__config_values[config_type] = config_value
                widget.manager.update_configs(self.__config_values)
                break

    def start_config_values(self, user_configs):
        self.__config_values = user_configs
        self.ids.text_input_box.start_configs(user_configs)
        self.ids.s1.value = self.__config_values["personal_configs"]['Font Size']
        self.ids.switch_scatter.active = self.__config_values["personal_configs"]['Scatter']

    def save_changes(self, change):
        if change:
            self.__config_values = {"Font Size": 15, "Font": "Times", "Scatter": True, 'Current Tab': None}
            self.ids.s1.value = self.__config_values['Font Size']
            self.ids.switch_scatter = self.__config_values['Scatter']

        self._popup.dismiss()

    def create_popup_save(self):
        content = ConfirmConfigs(save_changes=self.save_changes)
        self._popup = Popup( title='Deseja alterar para os valores padrão?', content=content,
                             size_hint=(None, None), size=(200, 200), pos=(100, 100), auto_dismiss=False)
        self._popup.open()

    def get_data(self, widget, widget_pos):
        if widget.focus:
            if self.__mask_values[widget_pos] == widget.text:
                widget.text = ""
        else:
            if widget.text == "":
                widget.text = self.__mask_values[widget_pos]
            self.__data_values[widget_pos] = widget.text


    @property
    def config_values(self):
        return self.__config_values

    @config_values.setter
    def config_values(self, values):
        self.__config_values = values


class ConfirmConfigs(FloatLayout):
    save_changes = ObjectProperty()


class TextInputBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.orientation = 'vertical'
        self.size_hint = None, None

        self.spacing = 5
        self.height_child = 50 + self.spacing
        self.__mask_values = {self.height_child * 6: "", self.height_child * 5: "Último Nome",
                              self.height_child * 4: "", self.height_child * 3: "Email",
                              self.height_child * 2: "Senha", self.height_child * 1: "Confirme a Senha"}

    def start_configs(self, user_configs):
        print(user_configs)
        for key, values in user_configs.items():
            print(key, values)
        self.__mask_values[self.height_child * 6] = user_configs["name"]

    def get_data(self, widget, widget_pos):
        print(self.__mask_values)
        if widget.focus:
            if self.__mask_values[widget_pos] == widget.text:
                widget.text = ""
        else:
            if widget.text == "":
                widget.text = self.__mask_values[widget_pos]
            #self.__data_values[widget_pos] = widget.text
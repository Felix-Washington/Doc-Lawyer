from kivy.properties import NumericProperty, ObjectProperty, ObservableDict

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.accordion import AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanelItem

import controller
from controller import UserMain
from controller.DocsManager import DocsManager
from controller.UserManagement import UserManagement
from kivy.config import Config


class WidowManager(ScreenManager):
    from controller.Login import Login
    from controller.UserMain import UserMain
    Builder.load_file( "widowmanager.kv" )
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    width: 1280
    height: 960
    Config.set( 'graphics', 'width', 1280 )
    Config.set( 'graphics', 'height',  960)

    def __init__(self, **kwargs):
        super( WidowManager, self ).__init__(**kwargs)
        self.__user_manager = UserManagement()
        self.__docs_manager = DocsManager()

    def update(self, *args):
       # print("parente", self.parent )
        #print("filho", self.children)
        with self.canvas:
            pass

    def user_docs(self, user):
        self.__docs_manager.load_docs(user)

    def call_create_buttons(self):

        for widget in self.walk():
            try:
                if type(widget) == AccordionItem:
                    widget.children[0].children[0].children[0].children[0].children[0].\
                        create_buttons(self.__docs_manager.documents)
                    break
            except Exception as e:
                pass


    def on_size(self, *args):
        #self.width = 1280
        self.update()
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height * 0.75
        #print( "Init W:" + str( self.perspective_point_x ) + "H:" + str( self.perspective_point_y ) )


class MainController(App):
    Config.set( 'input', 'mouse', 'mouse,multitouch_on_demand' )
    def build(self):

        return WidowManager()


if __name__ == '__main__':
    MainController().run()

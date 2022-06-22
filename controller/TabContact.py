from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanelItem


class TabContact(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        # Builder.load_file( "Kivy_Files/usermain.kv" )
        self.text = "Contato"


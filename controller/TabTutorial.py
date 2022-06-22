from kivy.uix.tabbedpanel import TabbedPanelItem


class TabTutorial(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        #E Builder.load_file( "Kivy_Files/usermain.kv" )
        self.text = "Tutorial"


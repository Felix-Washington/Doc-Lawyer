from controller.TabConfigs import TabConfigs
from controller.TabDocs import TabDocs
from controller.TabTutorial import TabTutorial
from controller.TabContact import TabContact
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel
import time


def decorator_teste(orig_func):
    def wrapper_function():
        start = time.time()
        orig_func()
        end = time.time()
        print("time", end-start)
    return wrapper_function


class UserMain( Screen ):
    Builder.load_file( "Kivy_Files/usermain.kv" )

    def __init__(self, **kw):
        super().__init__(**kw)

    def deslog(self):
        for widget in self.walk():
            if str(type(widget)) == "<class 'controller.TabDocs.AccordionArea'>":

                for acc_item in widget.children:
                    acc_item.clear_widgets()


        self.manager.deslog()


class Tab(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )

    def update_user_current_screen(self):
        for tab in self.tab_list:
            if tab.state == "normal":
                pass
                #self.parent.parent.manager.update_configs({"current_tab": str(tab)})
'''
        import tkinter as tk
        from tkinter import ttk
        from tkinter import filedialog as fd

        # Root window
        root = tk.Tk()
        root.title( 'Display a Text File' )
        root.resizable( False, False )
        root.geometry( '550x250' )

        # Text editor
        text = tk.Text( root, height=12 )
        text.grid( column=0, row=0, sticky='nsew' )

        def open_text_file():
            # file type
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
            # show the open file dialog
            f = fd.askopenfile( filetypes=filetypes )
            # read the text file and show its content on the Text
            text.insert( '1.0', f.readlines() )

        # open file button
        open_button = ttk.Button(
            root,
            text='Open a File',
            command=open_text_file
        )

        open_button.grid( column=0, row=1, sticky='w', padx=10, pady=10 )


        #if action == "close":
        #    popupWindow.close()

'''
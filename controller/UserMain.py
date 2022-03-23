import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix import filechooser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserLayout, FileSystemLocal
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelContent, TabbedPanelItem
from fpdf import FPDF

# @decorator_teste
from kivy.uix.togglebutton import ToggleButton


def decorator_teste(orig_func):
    def wrapper_function(*args, **kwargs):
        if orig_func.__name__ == "check_botao":
            print("")
        return orig_func( *args, **kwargs )

    return wrapper_function


class UserMain( Screen ):
    Builder.load_file( "usermain.kv" )

    def __init__(self, **kw):
        super().__init__( **kw )

        self.bind( children=self.update )
        self.bind( size=self.update )
        self.update()



    def update(self, *args):
        #print( self.parent )
        with self.canvas:
            pass

    def deslog(self):
        self.manager.current = "Login"


class Docs_Button(ToggleButton):
    def __init__(self, doc, **kwargs):
        super( Docs_Button, self ).__init__( **kwargs )
        self.size_hint = (None, None)
        self.size = (300, 50)
        self.doc = doc
        self.text = doc.name
        self.conteudo = doc.text
        self.group = "g1"




    def on_press(self):
        self.parent.check_botao( self )


class Table( BoxLayout ):
    def __init__(self, **kwargs):
        super( Table, self ).__init__( **kwargs )
        # self.bind( pos=self.update )

    def create_buttons(self, docs):
        #print(DocsManager().documents)
        for doc in docs:
            self.add_widget( Docs_Button( doc ) )



    def update(self, *args):
        with self.canvas:
            pass
    def check_botao(self, botao):
        # self.parent.parent.parent.parent.parent.parent.parent.children[0].update( botao.text )
        for widget in self.walk_reverse():
            if type(widget) == TabbedPanelContent:
                widget.children[0].children[0].children[0].children[0].update_label(botao)


class Text_Label(Label):
    pass


class Page(ScrollView):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )

    def update_label(self, button):
        self.children[0].text = button.conteudo


class Tab(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )


class FloatAreaButtons(GridLayout):
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        #self.popupWindow = None

    def download(self):
        # save FPDF() class into a
        # variable pdf
        self.show_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_popup(self):
        size = [500, 500]

        show = P(size)

        popupWindow = Popup(title="Escolha um arquivo", content=show, size_hint=(None, None),
                            size=size, auto_dismiss=False)

        popupWindow.open()
        # popup: 400/400
        # float: 375/340
        # gap: 25/60

    def close_popup(self):
        self.popupWindow.dismiss()

    def save_pdf(self):

        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font( "Arial", size=15 )

        # create a cell
        #pdf.cell( 200, 10, txt="GeeksforGeeks",
        #          ln=1, align='C' )

        # add another cell
        #pdf.cell( 200, 10, txt="A Computer Science portal for geeks.",
        #          ln=2, align='C' )

        # save the pdf with name .pdf
        pdf.output( "GFG.pdf" )
        pass

    def save(self, path, filename):
        with open( os.path.join( path, filename ), 'w' ) as stream:
            stream.write( self.text_input.text )

    def show_save(self):
        print(os.getcwd())
        content = SaveDialog( save=self.save, cancel=self.dismiss_popup )
        self._popup = Popup( title="Escolha a pasta", content=content,
                             size_hint=(0.9, 0.9) )
        self._popup.open()


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class P(FloatLayout):
    def __init__(self, size, **args):
        super().__init__( **args )
        self.size_hint = None, None
        self.size = size[0] - 25, size[1] - 60
        self.show_file_chooser()

    def back(self, widget):
        for wid in widget.walk_reverse():
            #print(type(wid))
            if type(wid) == Popup:
                #print(wid.root)
                wid.dismiss()


    def show_file_chooser(self):
        pass
        #f = FileChooser()
        #self.add_widget(f)
        #filechooser


class FileChooser(FileSystemLocal):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )



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
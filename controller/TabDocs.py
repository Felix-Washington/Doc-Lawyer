import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix import filechooser
from kivy.uix.accordion import Accordion
from kivy.uix.behaviors import ButtonBehavior

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelContent, TabbedPanelItem
from fpdf import FPDF
import time


def decorator_teste(*args, **kwargs):
    def wrapper_function(*args, orig_func, **kwargs):
        start = time.time()
        orig_func()
        end = time.time()
        print( "time", end - start )

    return wrapper_function


class TabDocs( TabbedPanelItem ):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.text = 'Docs'
        Builder.load_file( "Kivy_Files/tab_docs.kv" )

    def call_create_itens(self, doc_names, pdf_docs):
        self.ids.acc_area.create_itens( doc_names, pdf_docs )


class AccordionArea( Accordion ):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.size_hint = None, None
        self.size = 300, 900
        self.orientation = 'vertical'
        # Color red hex: #B87575

    # @decorator_teste
    def create_itens(self, doc_names, pdf_docs):
        child_number = 0
        #for category in doc_names.keys():
        #    acc_item = AccordionCategories

        for category in doc_names.keys():
            print( category )
            # Rename panel itens with doc_categories.
            self.children[::-1][child_number].title = category
            # Put images in AccItems
            self.children[::-1][child_number].background_normal = "imgs/acc_item_default.png"
            self.children[::-1][child_number].background_selected = "imgs/acc_item_selected.png"
            child_number += 1
        # Open first acc item
        self.children[-1].collapse = False

        self.create_buttons_in_acc_items( doc_names, pdf_docs )

    def create_buttons_in_acc_items(self, doc_names, pdf_docs):
        # Create buttons inside AccordionItems in their respective categories
        for child in reversed( self.children ):

            for category, value in pdf_docs.items():
                if child.title == category:
                    child.children[0].children[0].children[0].children[0].children[0].create_buttons(
                        pdf_docs[category] )
                    self.parent.children[0].children[0].children[0].create_pdf( pdf_docs[category] )


class Grid_Buttons( BoxLayout ):
    def __init__(self, **kwargs):
        super( Grid_Buttons, self ).__init__( **kwargs )

    def create_buttons(self, pdf_docs):
        for button_name in pdf_docs:
            self.add_widget( Docs_Button( button_name, pdf_docs[button_name] ) )

    def send_button_content(self, button_name):
        for widget in self.walk_reverse():
            if type( widget ) == TabbedPanelContent:
                widget.children[0].children[0].children[0].children[0].update_pdf( button_name )

    def teste(self):
        print(self.children)

class Docs_Button( ToggleButton ):
    enabled = BooleanProperty

    def __init__(self, button_name, pdf, **kwargs):
        super( Docs_Button, self ).__init__( **kwargs )
        self.size_hint = None, None
        self.size = (300, 50)
        self.text = button_name
        self.group = "g1"
        self.pdf_data = pdf

    def on_press(self):
        self.parent.send_button_content(self.text)


class PdfView( ScrollView ):
    source = StringProperty( '' )
    pdfpath = StringProperty( '' )

    def __init__(self, **kwargs):
        super( PdfView, self ).__init__( **kwargs )
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.always_overscroll = False
        self.current_pdf = None
        self.__box_pdf_pages = {}

    def create_pdf(self, pdfs):
        for doc_name, doc_path in pdfs.items():
            self.children[0].create_pdf( doc_name, doc_path )

    def update_pdf(self, pdf_data):
        self.children[0].clear_widgets()
        # for page_number, fil in pdf_data.items():
        self.children[0].update( pdf_data )


class BoxPdfPages( BoxLayout ):
    def __init__(self, **args):
        super().__init__( **args )
        self.orientation = "vertical"
        self.size_hint = None, None
        self.current_pdf = []
        self.count = 0
        self.__pdfs = {}
        self.__pdf_size = {}

    def create_pdf(self, button_name, pdf_pages_path):
        self.__pdfs[button_name] = pdf_pages_path
        self.__pdf_size[button_name] = len( pdf_pages_path.keys() )
        #  Kwargs: source=fil, index=page_num

    def update(self, name):
        self.size[1] = 870
        document = self.__pdfs[name]
        for index, value in document.items():
            pdf = PdfPage( self.size, index=index, source=value )
            self.add_widget( pdf )
        self.size[1] *= self.__pdf_size[name]


class PdfPage( ButtonBehavior, Factory.Image ):
    index = NumericProperty()

    def __init__(self, size, **kwargs):
        super().__init__( **kwargs )
        self.size_hint = None, None
        self.keep_ratio = True
        self.allow_stretch = True
        self.size = size

    def on_release(self, *args):
        # print(self.index)
        pass


class GridAreaButtons( GridLayout ):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )

    def dismiss_popup(self):
        self._popup.dismiss()

    def save(self, path, filename):
        try:
            assert os.path.isfile( path )
            with open( os.path.join( path ), 'w' ) as stream:
                stream.write( filename )

        except Exception as e:
            print( e )

    def show_save(self):
        print( os.getcwd() )
        content = SaveDialog( save=self.save, cancel=self.dismiss_popup )
        self._popup = Popup( title="Escolha a pasta", content=content,
                             size_hint=(None, None), size=(500, 500) )
        self._popup.open()


class SaveDialog( FloatLayout ):
    cancel = ObjectProperty()
    save = ObjectProperty()
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__( **kwargs )

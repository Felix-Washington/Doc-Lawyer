import os, fitz

from PyPDF2 import PdfFileReader
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock, NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix import filechooser
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.behaviors import ButtonBehavior

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelContent, TabbedPanelItem
from fpdf import FPDF


class TabDocs(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.text = 'Docs'
        Builder.load_file( "Kivy_Files/tab_docs.kv" )


class AccordionArea(Accordion):
    def __init__(self, **kwargs):
        super( AccordionArea, self ).__init__( **kwargs )
        self.size_hint = None, None
        self.size = 300, 900
        self.orientation = 'vertical'

        # Color red hex: #B87575

    def create_itens(self, doc_names, pdf_docs):
        child_number = 0
        for category in doc_names.keys():
            # Rename panel itens with doc_categories.
            self.children[::-1][child_number].title = category

            # Put images in AccItems
            self.children[::-1][child_number].background_normal = "imgs/acc_item_default.png"
            self.children[::-1][child_number].background_selected = "imgs/acc_item_selected.png"
            child_number += 1

        # Open first acc item
        self.children[-1].collapse = False

        # Create buttons inside AccordionItems in their respective categories
        for child in reversed(self.children):

            for category, button_name in doc_names.items():
                if child.title == category:
                    # Acess Grid_Buttons widget and create buttons.
                    child.children[0].children[0].children[0].children[0].children[0].create_buttons(pdf_docs[category])

                    self.parent.children[0].children[0].children[0].create_pdf(button_name, pdf_docs[category])

class Grid_Buttons( BoxLayout ):
    def __init__(self, **kwargs):
        super( Grid_Buttons, self ).__init__( **kwargs )

    def create_buttons(self, pdf_docs):
        for button_name in pdf_docs:
            self.add_widget( Docs_Button(button_name, pdf_docs[button_name]))

    def send_button_content(self, button_name, button_pdf_data):
        for widget in self.walk_reverse():
            if type(widget) == TabbedPanelContent:
                #if str(type(widget.children[0].children[0].children[0].children[0])) == "<class 'controller.TabDocs.PdfView'>":
                #widget.children[0].children[0].children[0].children[0].source = "test.pdf"
                widget.children[0].children[0].children[0].children[0].update_pdf(button_pdf_data)


class Docs_Button(ToggleButton):
    def __init__(self, button_name, pdf, **kwargs):
        super( Docs_Button, self ).__init__( **kwargs )
        self.size_hint = None, None
        self.size = (300, 50)
        self.text = button_name
        self.group = "g1"
        self.pdf_data = pdf

    def on_press(self):
        self.parent.send_button_content(self.text, self.pdf_data)


class GridAreaButtons(GridLayout):
    def __init__(self, **kwargs):
        super().__init__( **kwargs )
        self.size_hint = None, None
        self.cols = 3

    def dismiss_popup(self):
        self._popup.dismiss()

    def save_pdf(self):
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font( "Arial", size=15 )

        # create a cell
        # pdf.cell( 200, 10, txt="GeeksforGeeks",
        #          ln=1, align='C' )

        # save the pdf with name .pdf
        pdf.output( "GFG.pdf" )

    def save(self, path, filename):
        try:
            assert os.path.isfile(path)
            with open( os.path.join( path), 'w' ) as stream:
                stream.write( self.text_input.text )

        except Exception as e:
            print (e)
        # self.save_pdf()

    def show_save(self):
        print(os.getcwd())
        content = SaveDialog( save=self.save, cancel=self.dismiss_popup )
        self._popup = Popup( title="Escolha a pasta", content=content,
                             size_hint=(None, None), size=(500, 500) )
        self._popup.open()


class SaveDialog(FloatLayout):
    cancel = ObjectProperty()
    save = ObjectProperty()
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__( **kwargs )


class PdfView(ScrollView):
    source = StringProperty('')
    pdfpath = StringProperty('')

    def __init__(self, **kwargs):
        super(PdfView, self).__init__(**kwargs)

        self.do_scroll_x = False
        self.do_scroll_y = True
        self.always_overscroll = False
        self.current_pdf = None
        self.__box_pdf_pages = {}
        #self.add_widget(self.current_pdf)

    def create_pdf(self, doc_names, pdfs):
        #self.__box_pdf_pages[doc_names] = pdfs
        self.children[0].create_pdf()


    def update_pdf(self, pdf_data):
        self.children[0].clear_widgets()
        #for page_number, fil in pdf_data.items():
        #self.children[0].create_pdf(pages=pdf_data)


class BoxPdfPages(BoxLayout):
    def __init__(self, **args):
        super().__init__( **args )
        self.orientation = "vertical"
        self.size_hint = None, None
        self.current_pdf = []
        self.count = 0
        #self.children

    def create_pdf(self, **kwargs):
        #  Kwargs: source=fil, index=page_num
        #pages = kwargs["pages"]
        pass#print(kwargs)
        #for index, value in pages.items():
            #print(index, value)

            #pdf_page = PdfPage(self.size, index=index, source=value)
            #self.current_pdf.append(pdf_page)
            #self.add_widget(pdf_page)
        #


class PdfPage(ButtonBehavior, Factory.Image):
    index = NumericProperty()

    def __init__(self, size, **kwargs):
        super().__init__( **kwargs )

        self.size_hint = None, None
        self.keep_ratio = True
        self.allow_stretch = True
        self.size = size

    def on_release(self, *args):
        print(self.index)

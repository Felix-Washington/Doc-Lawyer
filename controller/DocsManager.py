import os
from datetime import date
import random

from PyPDF2 import PdfFileReader
from fitz import fitz

from model.DocModel import DocModel
from string import Template
import time


def decorator_teste(orig_func):
    def wrapper_function():
        start = time.time()
        orig_func()
        end = time.time()
        print( "time", end - start )

    return wrapper_function


class DocsManager:
    def __init__(self):
        self.__current_date = date.today().strftime( "%d/%m/%Y" )
        self.__texts_dict = {"Crime": {"assalto": "", "roubo": ""},
                             "Oficio": {"teste_of": "", "teste2": ""},
                             "Procuracao": {"proc": "", "proc_teste": ""}}

        # Get document names and link to respective category key.
        self.__doc_names = {}

        self.__pdf_dict = {}
        self.__pdf_path = ""

        # Relation of signatures and documents. How it works:
        # Signature type > Document category > document name.
        self.docs_in_signature = {"common":
                                  {"Crime": {"assalto": ""},
                                   "Oficio": {"teste_of": ""},
                                   "Procuracao": {"proc": ""}
                                   }, "master":
                                  {"Crime": {"assalto": "", "roubo": ""},
                                   "Oficio": {"teste_of": "", "teste2": ""},
                                   "Procuracao": {"proc": "", "proc_teste": ""}
                                   }}

    def check_user_signature(self, user_data):
        user_signature = self.docs_in_signature[user_data["type"]]
        for key, values in user_signature.items():
            for doc_name in values:
                # Insert category to dict avoiding a Key Error.
                self.__pdf_dict[key] = values
                self.__pdf_dict[key][doc_name] = self.return_pdf()

            self.__doc_names[key] = list(values)

    # Pdf section: functions used for pdf.
    '''**********************************************************************************'''

    def return_pdf(self):
        pdf_data = {}
        # Get document in folder.
        pdf_list = ["teste", "Modelo_de_Procuracao__Pessoa_Fisica"]
        choice = random.choice( pdf_list )
        source = os.path.abspath( f"pdfs/{choice}.pdf" )

        self.__pdf_path = os.path.abspath( "pdfs/converted_imgs" )
        if not os.path.exists( self.__pdf_path ):
            os.mkdir( self.__pdf_path )
        pages = self.getpdfpages( filename=source )

        for page_num in pages:
            # get the pux from the pages
            pix = pages[page_num][1]
            # save pdf page image in pdfpath
            fil = os.path.join( self.__pdf_path, f"{choice}{page_num}.png" )
            # verify if img already exist, else create it.
            pix.writePNG( fil ) if not os.path.exists( fil ) else None
            # add image in the scrollview boxlayout
            pdf_data[page_num] = fil

        # Pdf_data - [page_number] = document_path
        return pdf_data

    @staticmethod
    def getpdfpages(filename):
        """Get pdf pages as bytes."""
        filepath = os.path.abspath( filename )
        # get the quantity of pages
        pdf = PdfFileReader( open( filepath, 'rb' ) )
        get_num_pages = pdf.getNumPages()
        pages = dict()
        # open pdf file
        doc = fitz.open( filepath )

        for pageNum in range( get_num_pages ):
            # get the page by index
            page = doc.load_page( pageNum )
            # get byttes from image
            pix = page.get_pixmap()
            # remove the alpha channel 'cause fitz don't work with alpha
            pix1 = fitz.Pixmap( pix, 0 ) if pix.alpha else pix  # PPM does not support transparency
            # get image data in this case "ppm", but we can use "png", etc.
            imgdata = pix1.tobytes( output="ppm" )
            pages[pageNum] = [imgdata, pix]
        return pages

    '''**********************************************************************************'''

    # Getters and setters.
    '''**********************************************************************************'''

    @property
    def pdf_path(self):
        return self.__pdf_path

    @pdf_path.setter
    def pdf_path(self, value):
        self.__pdf_path = value

    @property
    def pdf_dict(self):
        return self.__pdf_dict

    @property
    def doc_names(self):
        return self.__doc_names

    '''**********************************************************************************'''

    # Unused functions
    '''**********************************************************************************'''

    # Create txt doc.
    def create_documents(self, user):
        text = ""
        documents_counter = 0

        for category, texts in self.__texts_dict.items():
            for text_name in texts:

                path = "pdfs/" + category + "/" + text_name + ".txt"
                # Load a .txt used as text of document
                with open( path, encoding="utf-8" ) as fobj:
                    for line in fobj:
                        text += line

                    # Add text from txt to dict
                    self.__texts_dict[category][text_name] = text
                    # Add templates to text, (name, date...)
                    text_in_template = self.add_template( self.__texts_dict[category][text_name], user )
                    # Create a doc Object, params(category, document name, document content)
                    doc = DocModel( category, self.__doc_names[category][documents_counter], text_in_template )
                    # Add doc to a list of documents
                    # self.__dict_documents[doc.category][doc.name] = doc

                    # Used to get every single document name
                    documents_counter += 1
                    # Reset text aux
                    text = ""

            # Reset counter aux
            documents_counter = 0

    def add_template(self, text, user):
        template = Template( text )
        template = template.substitute( name=user.user_data["name"], data=self.__current_date )
        return template

    '''
    docs_dict = {"Crime": {"assalto": DocModel, "roubo": DocModel},
                 "Oficio": {"teste_of": DocModel, "teste2": DocModel},
                 "Procuracao": {"proc": DocModel, "proc_teste": DocModel}}
    '''
    '''**********************************************************************************'''

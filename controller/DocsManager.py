from model.DocModel import DocModel
# from unidecode import unidecode
from string import Template
from controller.Templates import Templates


class DocsManager:
    def __init__(self):
        self.__documents = []
        self.__primary_key = 0
        self.templates = Templates()


    def create_model(self):
        text = "teste"
        doc = DocModel(text)
        self.__documents.append(doc)
        self.__primary_key += 1

    def docs_pattern(self, user):
        self.templates.texts(user)

        for i in range(len(self.templates.documents_names)):
            self.templates.texts(user)

            doc_name = self.templates.documents_names[i]
            doc_text = self.templates.documents[i]
            doc = DocModel(doc_name, doc_text)
            self.__documents.append(doc)

            #path = message + i.lower() + file_type

            #with open(path) as f:
            #    lines = f.readlines()

            '''
            for item in lines:
                if "$name" in item:
                    pass
                string_line = "".join(str(item))
            '''

            #string_line = "".join(str(item) for item in lines)




    def load_docs(self, user):
        self.docs_pattern(user)

    @property
    def documents(self):
        return self.__documents


    def oficio(self, user):
        text = Template(

            '''
                Vimos por meio deste, solicitar a Vossa Senhoria, autorização para proceder a
                doação dos bens discriminados nas TDIs/02 A e/ou B que consta neste protocolado, à
                $name.
                Justificamos a doação destes bens por não oferecerem condições de recuparação
                e tão pouco por não oferecerem as condições necessárias para o uso e segurança.
                Diante disto, a Comissão de Inservibilidade deste Estabelecimento de Ensino
                considerou-os inservíveis.

            '''
        )
        return text.substitute(name=user)
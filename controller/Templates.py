from string import Template
from datetime import date
from docx import Document



class Templates:
    def __init__(self):
        self.__documents = []
        self.__documents_names = ["Oficio", "Procuração"]

    def texts(self, user):
        oficio = '''
Vimos por meio deste, solicitar a Vossa Senhoria, autorização para proceder a
doação dos bens discriminados nas TDIs/02 A e/ou B que consta neste protocolado, à
$name.
Justificamos a doação destes bens por não oferecerem condições de recuparação
e tão pouco por não oferecerem as condições necessárias para o uso e segurança.
Diante disto, a Comissão de Inservibilidade deste Estabelecimento de Ensino
considerou-os inservíveis.
'''

        procuracao = '''
                Nome: $name \n
                Data Atual: $date \n
Neste modelo de procuração, são passados a um ou mais outorgantes:
poderes especiais para comprar e/ou vender bens móveis e imóveis, podendo para tanto,
assinar compromissos e obrigações, ajustar cláusulas, condições e preços; dar e receber
quaisquer garantias; pagar ou receber sinal, parcelas ou o todo; assinar os contratos e
escrituras necessárias, transmitindo direito, ação, posse e domínio; responder pela
evicção; receber quaisquer quantias decorrentes do uso dos poderes conferidos, dando
recibos e quitações; representar perante repartições públicas federais, estaduais e
municipais, autarquias, sociedades de economia mista, Cartórios de Notas, Registro
de Imóveis e Registro de Títulos e Documentos e onde mais necessário for; pagar
impostos e assinar guias, inclusive de transmissão; constituir advogado com poderes
da cláusula "ad judicia" com os mais amplos poderes em qualquer juízo, instância
ou tribunal; receber citação inicial; acordar, concordar, transigir e desistir; praticar,
enfim, todos os demais atos para o fiel cumprimento do presente mandato, inclusive
substabelecer.
NOTA
1. Código Civil art. 496. É anulável a venda de ascendente a descendente, salvo se os
outros descendentes e o cônjuge do alienante expressamente houverem consentido.
Parágrafo único. Em ambos os casos, dispensa-se o consentimento do cônjuge se o
regime de bens for o da separação obrigatória.
            '''

        self.__documents.append(oficio)
        self.__documents.append(procuracao)
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        count = 0
        for document_number in range(len(self.__documents_names)):
            # 70 chars in a line


            template = self.add_template(self.__documents[document_number], user, today, count)
            #template.center(50)
            count += 1
            self.format_text(template)
            self.__documents[document_number] = template

    def add_template(self, doc, *args):
        template = Template( doc )

        #print("args", args[2])
        template = template.substitute( name=args[0], date=args[1])
        return template

    def format_text(self, text):
        line = text.splitlines()
        #print(line)

    @property
    def documents_names(self):
        return self.__documents_names

    @property
    def documents(self):
        return self.__documents

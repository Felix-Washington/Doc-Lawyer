
class DocModel:
    def __init__(self, name, text):
        self.__name = name
        self.__text = text

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
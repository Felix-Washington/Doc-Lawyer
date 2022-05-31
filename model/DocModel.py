
class DocModel:
    def __init__(self, category, name, text):
        self.__category = category
        self.__name = name
        self.__text = text

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category):
        self.__category = category

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

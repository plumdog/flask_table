from flask_table import Table, Col


class Item(object):
    def __init__(self, name, language):
        self.name = name
        self.language = language


class LangCol(Col):
    def td_format(self, content):
        if content == 'en_GB':
            return 'British English'
        elif content == 'de_DE':
            return 'German'
        elif content == 'fr_FR':
            return 'French'
        else:
            return 'Not Specified'


class ItemTable(Table):
    name = Col('Name')
    language = LangCol('Language')


def main():
    items = [Item('A', 'en_GB'),
             Item('B', 'de_DE'),
             Item('C', 'fr_FR'),
             Item('D', None)]

    tab = ItemTable(items)

    # or {{ tab }} in jinja
    print(tab.__html__())

if __name__ == '__main__':
    main()

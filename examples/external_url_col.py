from flask_table import Table, Col
from flask_table.html import element


class Item(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url


class ExternalURLCol(Col):
    def __init__(self, name, url_attr, **kwargs):
        self.url_attr = url_attr
        super(ExternalURLCol, self).__init__(name, **kwargs)

    def td_contents(self, item, attr_list):
        text = self.from_attr_list(item, attr_list)
        url = self.from_attr_list(item, [self.url_attr])
        return element('a', {'href': url}, content=text)


class ItemTable(Table):
    url = ExternalURLCol('URL', url_attr='url', attr='name')


def main():
    items = [
        Item('Google', 'https://google.com'),
        Item('Yahoo', 'https://yahoo.com'),
    ]

    tab = ItemTable(items)
    print(tab.__html__())

if __name__ == '__main__':
    main()

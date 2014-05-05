from flask_table import Table, Col


"""Lets suppose that we have a class that we get an iterable of from
somewhere, such as a database. We can declare a table that pulls out
the relevant entries, escapes them and displays them.

"""


class Item(object):
    def __init__(self, name, category):
        self.name = name
        self.category = category


class Category(object):
    def __init__(self, name):
        self.name = name


class ItemTable(Table):
    name = Col('Name')
    category_name = Col('Category', attr_list=['category', 'name'])
    # Equivalently: Col('Category', attr='category.name')
    # Both syntaxes are kept as the second is more readable, but
    # doesn't cover all options. Such as if the items are dicts and
    # the keys have dots in.


def main():
    items = [Item('A', Category('catA')),
             Item('B', Category('catB'))]

    tab = ItemTable(items)
    print(tab.__html__())

if __name__ == '__main__':
    main()

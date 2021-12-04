from flask_table import Table, Col, LinkCol
from flask import Flask, url_for

"""A example for creating a simple table within a working Flask app.

This table has two columns, linking to two different pages. Then a
subclass of LinkCol to conditionally select the target endpoint.

"""

app = Flask(__name__)


class LinkDeciderCol(LinkCol):

    def url(self, item):
        if item.name == 'B':
            endpoint = self.endpoint['b']
        else:
            endpoint = self.endpoint['a']
        return url_for(endpoint, **self.url_kwargs(item))


class ItemTable(Table):
    name = Col('Name')
    link_a = LinkCol(
        'Link A',
        'single_item_a',
        url_kwargs=dict(id='id'))
    link_b = LinkCol(
        'Link B',
        'single_item_b',
        url_kwargs=dict(id='id'))
    link_decider = LinkDeciderCol(
        'Decider Col',
        {'a': 'single_item_a',
         'b': 'single_item_b'},
        url_kwargs=dict(id='id'))


@app.route('/')
def index():
    items = Item.get_elements()
    table = ItemTable(items)
    return table.__html__()


@app.route('/item_a/<int:id>')
def single_item_a(id):
    element = Item.get_element_by_id(id)
    return '<h1>A: {}</h1><hr><small>id: {}</small>'.format(
        element.name, element.id)


@app.route('/item_b/<int:id>')
def single_item_b(id):
    element = Item.get_element_by_id(id)
    return '<h1>B: {}</h1><hr><small>id: {}</small>'.format(
        element.name, element.id)


class Item(object):
    """ a little fake database """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_elements(cls):
        return [
            Item(1, 'Z'),
            Item(2, 'K'),
            Item(3, 'B')]

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]


if __name__ == '__main__':
    app.run(debug=True)

from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)


class SortableTable(Table):
    id = Col('ID')
    name = Col('Name')
    description = Col('Description')
    link = LinkCol(
        'Link', 'flask_link', url_kwargs=dict(id='id'), allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()


@app.route('/item/<int:id>')
def flask_link(id):
    element = Item.get_element_by_id(id)
    return '<h1>{}</h1><p>{}</p><hr><small>id: {}</small>'.format(
        element.name, element.description, element.id)


class Item(object):
    """ a little fake database """
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def get_elements(cls):
        return [
            Item(1, 'Z', 'zzzzz'),
            Item(2, 'K', 'aaaaa'),
            Item(3, 'B', 'bbbbb')]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]

if __name__ == '__main__':
    app.run(debug=True)

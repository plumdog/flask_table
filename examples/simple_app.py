from flask_table import Table, Col, LinkCol
from flask import Flask

"""A example for creating a simple table within a working Flask app.

Our table has just two columns, one of which shows the name and is a
link to the item's page. The other shows the description.

"""

app = Flask(__name__)


class ItemTable(Table):
    name = LinkCol('Name', 'single_item',
                   url_kwargs=dict(id='id'), attr='name')
    description = Col('Description')


@app.route('/')
def index():
    items = Item.get_elements()
    table = ItemTable(items)

    # You would usually want to pass this out to a template with
    # render_template.
    return table.__html__()


@app.route('/item/<int:id>')
def single_item(id):
    element = Item.get_element_by_id(id)
    # Similarly, normally you would use render_template
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
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]


if __name__ == '__main__':
    app.run(debug=True)

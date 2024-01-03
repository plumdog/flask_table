import random

from flask_table import Table, Col, ButtonCol
from flask import Flask, request

app = Flask(__name__)

CHARS = [str(i) for i in range(10)]


def get_csrf_token():
    # You should replace this with the token generator for the csrf
    # mechanism you are using.
    return ''.join(random.choice(CHARS) for i in range(20))


@app.route('/')
def index():
    items = Item.get_elements()
    table = get_table_class()(items)
    return table.__html__()


@app.route('/item/<int:id>', methods=['POST'])
def single_item(id):
    element = Item.get_element_by_id(id)
    return (
        '<h1>{}</h1><p>{}</p><hr><small>id: {}</small>'
        '<p>CSRF token: {}</p>'
    ).format(
        element.name,
        element.description,
        element.id,
        request.form['csrf_token'],
    )


def get_table_class():
    csrf_token = get_csrf_token()

    class ItemTable(Table):
        name = Col('Name')
        description = Col('Description')
        button = ButtonCol(
            'Button',
            'single_item',
            url_kwargs=dict(id='id'),
            form_hidden_fields=dict(csrf_token=csrf_token)
        )
    return ItemTable


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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request

"""
A example for creating a Table that is sortable by it's header
"""

app = Flask(__name__)


class SortableTable(Table):
    id = Col("ID")
    name = Col('Name')
    description = Col('Description')
    link_id = LinkCol('Link', "flask_link", url_kwargs={'id': 'id'})

    def __init__(self, data, sort, *args, **kwargs):
        super(SortableTable, self).__init__(data)
        self.sort = sort

    # implementation of the sortable header
    def th(self, col_id, col):
        escaped = Markup.escape(col.name)
        if isinstance(col, LinkCol):
            th = escaped  # don't add the sort to the link column
        else:
            if self.sort == col_id:
                th = u"↓{}".format(escaped)
            else:
                th = u"<a href='?sort={}'>{}</a>".format(col_id, escaped)
        return u"<th>{}</th>".format(th)


@app.route("/")
def index():
    sort = request.args.get("sort", "id")
    table = SortableTable(Item.get_sorted_by(sort), sort)
    return table.__html__()


@app.route("/item/<int:id>")
def flask_link(id):
    element = Item.get_element_by_id(id)
    return "<h1>{}</h1><p>{}</p><hr><small>id: {}</small>".format(
        element.name, element.description, element.id)


class Item(object):
    """ a little fake database """
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.link_id = None  # this seems to be a ugly hack?!

    @classmethod
    def get_elements(cls):
        return [
            Item(1, 'Z', 'zzzzz'),
            Item(2, 'K', 'aaaaa'),
            Item(3, 'B', 'bbbbb'),
        ]

    @classmethod
    def get_sorted_by(cls, sort):
        return sorted(cls.get_elements(), key=lambda x: getattr(x, sort))

    @classmethod
    def get_element_by_id(cls, id):
        return filter(lambda x: x.id == id, cls.get_elements())[0]

if __name__ == '__main__':
    app.run(debug=True)

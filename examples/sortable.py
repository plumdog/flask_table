#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for

"""
A example for creating a Table that is sortable by it's header
"""

app = Flask(__name__)
app.DEBUG = True

class SortableTable(Table):
    id = Col("ID")
    name = Col('Name')
    description = Col('Description')
    link = LinkCol('Link', "flask_link", url_kwargs={'id': 'id'})

    def __init__(self, data, sort, reverse, *args, **kwargs):
        super(SortableTable, self).__init__(data)
        self.sort = sort
        self.reverse = reverse

    # implementation of the sortable header
    def th(self, col_id, col):
        escaped = Markup.escape(col.name)
        if col_id == 'link':
            th = escaped  # don't add the sort to the link column
        else:
            if self.sort == col_id:
                if self.reverse:
                    th = u"<a href='{}'>↑{}</a>".format(url_for('index', sort=col_id), escaped)
                else:
                    th = u"<a href='{}'>↓{}</a>".format(url_for('index', sort=col_id, direction='desc'), escaped)
            else:
                th = u"<a href='{}'>{}</a>".format(url_for('index', sort=col_id), escaped)
        return u"<th>{}</th>".format(th)


@app.route("/")
def index():
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse), sort, reverse)
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

    @classmethod
    def get_elements(cls):
        return [
            Item(1, 'Z', 'zzzzz'),
            Item(2, 'K', 'aaaaa'),
            Item(3, 'B', 'bbbbb'),
        ]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(cls.get_elements(), key=lambda x: getattr(x, sort), reverse=reverse)

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]

if __name__ == '__main__':
    app.run(debug=True)

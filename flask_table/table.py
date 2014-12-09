# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

from flask import Markup

from .columns import Col
from .compat import with_metaclass


class TableMeta(type):
    """The metaclass for the Table class. We use the metaclass to sort of
    the columns defined in the table declaration.

    """

    def __new__(meta, name, bases, attrs):
        """Create the class as normal, but also iterate over the attributes
        set and gather up any that are Cols, and store them, so they
        can be iterated over later.

        """
        cls = type.__new__(meta, name, bases, attrs)
        cols = [(k, v) for k, v in attrs.items() if isinstance(v, Col)]
        cls._cols = OrderedDict(sorted(cols, key=lambda x: x[1]._counter_val))
        return cls


class Table(with_metaclass(TableMeta)):
    """The main table class that should be subclassed when to create a
    table. Initialise with an iterable of objects. Then either use the
    __html__ method, or just output in a template to output the table
    as html. Can also set a list of classes, either when declaring the
    table, or when initialising.

    """

    classes = []
    allow_sort = False

    def __init__(self, items, classes=None, sort_by=None, sort_reverse=False):
        self.items = items
        self.sort_by = sort_by
        self.sort_reverse = sort_reverse
        if classes is not None:
            self.classes = classes

    def classes_html_attr(self):
        if not self.classes:
            return ''
        else:
            return ' class="{}"'.format(' '.join(self.classes))

    def __html__(self):
        tbody = self.tbody()
        if tbody:
            return '<table{attrs}>\n{thead}\n{tbody}\n</table>'.format(
                attrs=self.classes_html_attr(),
                thead=self.thead(),
                tbody=tbody)
        else:
            return '<p>No Items</p>'

    def thead(self):
        return '<thead><tr>{}</tr></thead>'.format(''.join(
            (self.th(col_key, col) for col_key, col in self._cols.items())))

    def tbody(self):
        out = []
        for i in self.items:
            out.append(self.tr(i))
        if out:
            return '<tbody>\n{}\n</tbody>'.format('\n'.join(out))
        else:
            return ''

    def tr(self, i):
        out = []
        for attr, c in self._cols.items():
            out.append(c.td(i, attr))
        return '<tr>{}</tr>'.format(''.join(out))

    def th_contents(self, col_key, col):
        escaped = Markup.escape(col.name)
        if not (col.allow_sort and self.allow_sort):
            return escaped

        if self.sort_by == col_key:
            if self.sort_reverse:
                return '<a href="{}">↑{}</a>'.format(
                    self.sort_url(col_key), escaped)
            else:
                return '<a href="{}">↓{}</a>'.format(
                    self.sort_url(col_key, reverse=True), escaped)
        else:
            return '<a href="{}">{}</a>'.format(
                self.sort_url(col_key), escaped)

    def th(self, col_key, col):
        return '<th>{}</th>'.format(self.th_contents(col_key, col))

    def sort_url(self, col_id, reverse=False):
        raise NotImplementedError('sort_url not implemented')

    @classmethod
    def add_column(cls, name, col):
        cls._cols[name] = col
        return cls


def create_table(name=str('_Table')):
    """Creates and returns a new table class. You can specify a name for
    you class if you wish.

    """
    return type(name, (Table,), {})

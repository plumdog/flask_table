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
        cls._cols = OrderedDict()
        # If there are any base classes with a `_cols` attribute, add
        # them to the columns for this table.
        for parent in bases:
            try:
                parent_cols = parent._cols
            except AttributeError:
                continue
            else:
                cls._cols.update(parent_cols)
        # Then add the columns from this class.
        this_cls_cols = sorted(
            ((k, v) for k, v in attrs.items() if isinstance(v, Col)),
            key=lambda x: x[1]._counter_val)
        cls._cols.update(OrderedDict(this_cls_cols))
        return cls


class Table(with_metaclass(TableMeta)):
    """The main table class that should be subclassed when to create a
    table. Initialise with an iterable of objects. Then either use the
    __html__ method, or just output in a template to output the table
    as html. Can also set a list of classes, either when declaring the
    table, or when initialising. Can also set the text to display if
    there are no items to display.

    """

    classes = []
    thead_classes = []
    allow_sort = False
    no_items = 'No Items'

    def __init__(self, items, classes=None, thead_classes=None,
                 sort_by=None, sort_reverse=False, no_items=None,
                 table_id=None):
        self.items = items
        self.sort_by = sort_by
        self.sort_reverse = sort_reverse
        if classes is not None:
            self.classes = classes
        if thead_classes is not None:
            self.thead_classes = thead_classes
        if no_items is not None:
            self.no_items = no_items
        self.table_id = table_id

    def classes_html_attr(self):
        s = ''
        if self.table_id:
            s += ' id="{}"'.format(self.table_id)
        if self.classes:
            s += ' class="{}"'.format(' '.join(self.classes))
        return s

    def thead_classes_html_attr(self):
        if not self.thead_classes:
            return ''
        else:
            return ' class="{}"'.format(' '.join(self.thead_classes))

    def __html__(self):
        tbody = self.tbody()
        if tbody:
            return '<table{attrs}>\n{thead}\n{tbody}\n</table>'.format(
                attrs=self.classes_html_attr(),
                thead=self.thead(),
                tbody=tbody)
        else:
            return '<p>{}</p>'.format(self.no_items)

    def thead(self):
        return '<thead{attrs}><tr>{ths}</tr></thead>'.format(
            attrs=self.thead_classes_html_attr(),
            ths=''.join(
                (self.th(col_key, col) for col_key, col in self._cols.items()
                 if col.show)))

    def tbody(self):
        out = [self.tr(item) for item in self.items]
        if out:
            return '<tbody>\n{}\n</tbody>'.format('\n'.join(out))
        else:
            return ''

    def tr_format(self, item):
        """Returns the string that is formatted with the contents of the
        tr. Override this if you want to alter the attributes of the
        tr.

        """

        return '<tr>{}</tr>'

    def tr(self, item):
        return self.tr_format(item).format(
            ''.join(c.td(item, attr) for attr, c in self._cols.items()
                    if c.show))

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


def create_table(name=str('_Table'), base=Table):
    """Creates and returns a new table class. You can specify a name for
    you class if you wish. You can also set the base class (or
    classes) that should be used when creating the class.

    """
    try:
        base = tuple(base)
    except TypeError:
        # Then assume that what we have is a single class, so make it
        # into a 1-tuple.
        base = (base,)
    return TableMeta(name, base, {})

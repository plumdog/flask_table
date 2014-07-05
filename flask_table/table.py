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

    def __init__(self, items, *, classes=None, sort_by=None, sort_reverse=False):
        self.items = items
        self.sort_by = sort_by
        self.sort_reverse = sort_reverse
        if classes is not None:
            self.classes = classes

    def classes_html_attr(self):
        if not self.classes:
            return ''
        else:
            return ' class="%s"' % ' '.join(self.classes)

    def __html__(self):
        if len(self.items) == 0:
            return '<p>No Items</p>'
        else:
            return '<table%s>%s\n%s</table>' % (
                self.classes_html_attr(),
                self.thead(), self.tbody())

    def thead(self):
        return '<thead><tr>%s</tr></thead>' % ''.join(
            (self.th(col_key, col) for col_key, col in self._cols.items())
        )

    def tbody(self):
        out = []
        for i in self.items:
            out.append(self.tr(i))
        return '<tbody>%s</tbody>' % ''.join(out)

    def tr(self, i):
        out = []
        for attr, c in self._cols.items():
            out.append(c.td(i, attr))
        return '<tr>%s</tr>' % ''.join(out)

    def th_contents(self, col_key, col):
        escaped = Markup.escape(col.name)
        if not (col.allow_sort and self.allow_sort):
            return escaped

        if self.sort_by == col_key:
            if self.sort_reverse:
                return u'<a href="{}">↑{}</a>'.format(self.sort_url(col_key), escaped)
            else:
                return u'<a href="{}">↓{}</a>'.format(self.sort_url(col_key, reverse=True), escaped)
        else:
            return u'<a href="{}">{}</a>'.format(self.sort_url(col_key), escaped)

    def th(self, col_key, col):
        return u'<th>{}</th>'.format(self.th_contents(col_key, col))

    def sort_url(self, col_id, reverse=False):
        raise NotImplementedError('sort_url not implemented')

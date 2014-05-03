from collections import OrderedDict
from flask import Markup
from .columns import Col


class TableMeta(type):
    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        cols = [(k,v) for k,v in attrs.items() if isinstance(v, Col)]
        cls._cols = OrderedDict(sorted(cols, key=lambda x: x[1]._counter_val))
        return cls

class Table(object, metaclass=TableMeta):
    def __init__(self, items=None, classes=['table']):
        self.items = items
        self.classes = classes

    def cols(self):
        return self._cols

    def classes_html_attr(self):
        if not self.classes:
            return ''
        else:
            return ' class="%s"' % ' '.join(self.classes)

    def __html__(self):
        if len(self.items) == 0:
            return '<p>No Items</p>'
        else:
            return '<table%s>%s\n%s</table>' % (self.classes_html_attr(), self.thead(), self.tbody())

    def thead(self):
        out = []
        for h in self.cols().values():
            out.append('<th>%s</th>' % Markup.escape(h.name))
        return '<thead><tr>%s</tr></thead>' % ''.join(out)

    def tbody(self):
        out = []
        for i in self.items:
            out.append(self.tr(i))
        return '<tbody>%s</tbody>' % ''.join(out)

    def tr(self, i):
        out = []
        for attr, c in self.cols().items():
            out.append(c.td(i, attr))
        return '<tr>%s</tr>' % ''.join(out)

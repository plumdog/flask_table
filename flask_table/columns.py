from flask import Markup, url_for
from babel.dates import format_date, format_datetime

def _recursive_getattr(item, keys):
    if item is None:
        return None
    if len(keys) == 1:
        return getattr(item, keys[0])
    else:
        return _recursive_getattr(getattr(item, keys[0]), keys[1:])

class Col(object):
    _counter = 0
    def __init__(self, name, attr=None, attr_list=[]):
        self.name = name
        self._counter_val = Col._counter
        self.attr = attr
        self.attr_list = attr_list
        Col._counter += 1

    @classmethod
    def gettype(cls):
        return cls.__name__

    def get_attr_list(self, attr):
        if self.attr:
            return [self.attr]
        elif self.attr_list:
            return self.attr_list
        elif attr:
            return [attr]
        else:
            return None

    def from_attr_list(self, i, attr_list):
        out = _recursive_getattr(i, attr_list)
        if out is None:
            return ''
        else:
            return out

    def td(self, i, attr):
        return '<td>' + self.td_contents(i, self.get_attr_list(attr)) + '</td>'

    def td_contents(self, i, attr_list):
        return self.td_format(self.from_attr_list(i, attr_list))

    def td_format(self, content):
        return str(Markup.escape(str(content)))

class BoolCol(Col):
    def td_format(self, content):
        if content:
            return 'Yes'
        else:
            return 'No'

class DateCol(Col):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.date_format = kwargs.get('date_format', 'short')

    def td_format(self, content):
        if content:
            return format_date(content, self.date_format)
        else:
            return ''

class DatetimeCol(Col):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.datetime_format = kwargs.get('datetime_format', 'short')

    def td_format(self, content):
        if content:
            return format_datetime(content, self.datetime_format)
        else:
            return ''


class LinkCol(Col):
    def __init__(self, name, endpoint, attr=None, attr_list=[], url_kwargs={}):
        super().__init__(name, attr=attr, attr_list=attr_list)
        self.endpoint = endpoint
        self._url_kwargs = url_kwargs

    def url_kwargs(self, item):
        url_kwargs_out = {}
        for k,v in self._url_kwargs.items():
            url_kwargs_out[k] = getattr(item, v)
        return url_kwargs_out

    def get_attr_list(self, attr):
        return super().get_attr_list(None)

    def text(self, i, attr_list):
        if attr_list:
            return self.from_attr_list(i, attr_list)
        else:
            return self.name
        

    def url(self, i):
        return url_for(self.endpoint, **self.url_kwargs(i))

    def td_contents(self, i, attr_list):
        return '<a href="%s">%s</a>' % (self.url(i), Markup.escape(self.text(i, attr_list)))

                
class ButtonCol(LinkCol):
    def td_contents(self, i, attr_list):
        return '<form method="post" action="%s"><button type="submit">%s</button></form>' % (self.url(i), Markup.escape(self.text(i, attr_list)))

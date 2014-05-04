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
    """The subclass for all Columns, and the class that just gets some
    data from each item an outputs it.

    We use this hack with _counter to make sure that the columns end
    up in the same order as when declared. Each column must set a
    name, which is used in as the heading for that column, and can
    optionally set an attr or an attr_list. attr='foo' is equivalent
    to attr_list=['foo'] and attr_list=['foo', 'bar', 'baz'] will
    attempt to get item.foo.bar.baz for each item in the iterable
    given to the table. If item.foo.bar is None, then this process
    will terminate and will not error. However, if item.foo.bar is an
    object without an attribute 'baz', then this will currently error.

    """

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
        return '<td>%s</td>' % self.td_contents(i, self.get_attr_list(attr))

    def td_contents(self, i, attr_list):
        """Given an item and an attr_list, return the contents of the
        <td>.

        This method is a likely candidate to override when extending
        the Col class, which is done in LinkCol and
        ButtonCol. Override this method if you need to get some extra
        data from the item.

        Note that the output of this function is NOT escaped.

        """
        return self.td_format(self.from_attr_list(i, attr_list))

    def td_format(self, content):
        """Given just the value extracted from the item, return what should
        appear within the td.

        This method is also a good choice to override when extending,
        which is done in the BoolCol, DateCol and DatetimeCol
        classes. Override this method when you just need the standard
        data that attr_list gets from the item, but need to adjust how
        it is represented.

        Note that the output of this function is NOT escaped.

        """
        return str(Markup.escape(str(content)))


class BoolCol(Col):
    """If the content is truthy, then output Yes. Otherwise output No.

    TODO: generalise to a dict of options, plus a default.
    TODO: account for internationalisation.

    """
    def td_format(self, content):
        if content:
            return 'Yes'
        else:
            return 'No'


class DateCol(Col):
    """Format the content as a date, unless it is None, in which case,
    output empty.

    """
    def __init__(self, name, **kwargs):
        Col.__init__(self, name, **kwargs)
        self.date_format = kwargs.get('date_format', 'short')

    def td_format(self, content):
        if content:
            return format_date(content, self.date_format)
        else:
            return ''


class DatetimeCol(Col):
    """Format the content as a datetime, unless it is None, in which case,
    output empty.

    """
    def __init__(self, name, **kwargs):
        Col.__init__(self, name, **kwargs)
        self.datetime_format = kwargs.get('datetime_format', 'short')

    def td_format(self, content):
        if content:
            return format_datetime(content, self.datetime_format)
        else:
            return ''


class LinkCol(Col):
    """Format the content as a link. Requires a endpoint to use to find
    the url and can also take a dict of url_kwargs which is expected
    to have values that are strings which are used to get data from
    the item.

    Eg:

    view = LinkCol('View', 'view_fn', url_kwargs=dict(id='id'))

    This will create a link to the address given by url_for('view_fn',
    id=item.id) for each item in the iterable.

    """
    def __init__(self, name, endpoint, attr=None, attr_list=[], url_kwargs={}):
        Col.__init__(self, name, attr=attr, attr_list=attr_list)
        self.endpoint = endpoint
        self._url_kwargs = url_kwargs

    def url_kwargs(self, item):
        url_kwargs_out = {}
        for k, v in self._url_kwargs.items():
            # TODO: replate getattr with _recursive_getattr, to
            # maintain consistency.
            url_kwargs_out[k] = getattr(item, v)
        return url_kwargs_out

    def get_attr_list(self, attr):
        return Col.get_attr_list(self, None)

    def text(self, i, attr_list):
        if attr_list:
            return self.from_attr_list(i, attr_list)
        else:
            return self.name

    def url(self, i):
        return url_for(self.endpoint, **self.url_kwargs(i))

    def td_contents(self, i, attr_list):
        return '<a href="%s">%s</a>' % (self.url(i),
                                        Markup.escape(self.text(i, attr_list)))


class ButtonCol(LinkCol):
    """Just the same a LinkCol, but creates an empty form which gets
    posted to the specified url.

    Eg:

    delete = ButtonCol('Delete', 'delete_fn', url_kwargs=dict(id='id'))

    When clicked, this will post to url_for('delete_fn', id=item.id).

    """

    def td_contents(self, i, attr_list):
        return ('<form method="post" action="%s">'
                '<button type="submit">%s</button>'
                '</form>') % (self.url(i),
                              Markup.escape(self.text(i, attr_list)))

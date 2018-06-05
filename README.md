Flask Table
===========

Because writing HTML is fiddly and all of your tables are basically
the same.

[![Build Status](https://travis-ci.org/plumdog/flask_table.svg?branch=master)](https://travis-ci.org/plumdog/flask_table)
[![Coverage Status](https://coveralls.io/repos/plumdog/flask_table/badge.png?branch=master)](https://coveralls.io/r/plumdog/flask_table?branch=master)
[![PyPI version](https://badge.fury.io/py/Flask-Table.svg)](https://badge.fury.io/py/Flask-Table)

Installation
============
```
pip install flask-table
```

Quick Start
===========

```python
# import things
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')

# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
items = [Item('Name1', 'Description1'),
         Item('Name2', 'Description2'),
         Item('Name3', 'Description3')]
# Or, equivalently, some dicts
items = [dict(name='Name1', description='Description1'),
         dict(name='Name2', description='Description2'),
         dict(name='Name3', description='Description3')]

# Or, more likely, load items from your database with something like
items = ItemModel.query.all()

# Populate the table
table = ItemTable(items)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template
```

Which gives something like:

```html
<table>
<thead><tr><th>Name</th><th>Description</th></tr></thead>
<tbody>
<tr><td>Name1</td><td>Description1</td></tr>
<tr><td>Name2</td><td>Description2</td></tr>
<tr><td>Name3</td><td>Description3</td></tr>
</tbody>
</table>
```

Or as HTML:

<table>
<thead><tr><th>Name</th><th>Description</th></tr></thead>
<tbody>
<tr><td>Name1</td><td>Description1</td></tr>
<tr><td>Name2</td><td>Description2</td></tr>
<tr><td>Name3</td><td>Description3</td></tr>
</tbody>
</table>

For more, see [the examples](#the-examples) for some complete,
runnable demonstrations.

Extra things:
-------------

* The attribute used for each column in the declaration of the column
  is used as the default thing to lookup in each item.

* The thing that you pass when you populate the table must:
  * be iterable
  * contain dicts or objects - there's nothing saying it can't contain
    some of each. See `examples/simple_sqlalchemy.py` for a database
    example.

* You can pass attributes to the `td` and `th` elements by passing a
  dict of attributes as `td_html_attrs` or `th_html_attrs` when creating a
  Col. Or as `column_html_attrs` to apply the attributes to both the `th`s
  and the `td`s. (Any that you pass in `th_html_attrs` or `td_html_attrs` will
  overwrite any that you also pass with `column_html_attrs`.) See
  examples/column_html_attrs.py for more.

* There are also LinkCol and ButtonCol that allow links and buttons,
  which is where the Flask-specific-ness comes in.

* There are also DateCol and DatetimeCol that format dates and
  datetimes.

* Oh, and BoolCol, which does Yes/No.

* But most importantly, Col is easy to subclass.

Table configuration and options
===============================

The following options configure table-level options:

* `thead_classes` - a list of classes to set on the `<thead>` element.

* `no_items` - a string to display if no items are passed, defaults to
  `'No Items'`.

* `html_attrs` - a dictionary of attributes to set on the `<table>` element.

* `classes` - a list of strings to be set as the `class` attribute on
  the `<table>` element.

* `table_id` - a string to set as the `id` attribute on the `<table>` element.

* `border` - whether the `border` should be set on the `<table>` element.

These can be set in a few different ways:

a) set when defining the table class
```python
class MyTable
    classes = ['class1', 'class2']
```

b) passed in the `options` argument to `create_table`.
```python
MyTable = create_table(options={'table_id': 'my-table-id'})
```

c) passed to the table's `__init__`
```python
table = MyTable(items, no_items='There is nothing', ...)
```

Note that a) and b) define an attribute on the table class, but c)
defines an attribute on the instance, so anything set like in c) will
override anything set in a) or b).

Eg:
```python
class ItemTable(Table):
    classes = ['myclass']
    name = Col('Name')
table = ItemTable(items, classes=['otherclass'])
```
would create a table with `class="otherclass"`.

Included Col Types
==================

* [`OptCol`](#more-about-optcol) - converts values according to a
  dictionary of choices. Eg for turning stored codes into human
  readable text.

* [`BoolCol`](#more-about-boolcol) (subclass of OptCol) - converts
  values to yes/no.

* [`BoolNaCol`](#more-about-boolnacol) (subclass of BoolCol) - converts
  values to yes/no/na.

* [`DateCol`](#more-about-datecol) - for dates (uses `format_date`
  from `babel.dates`).

* [`DatetimeCol`](#more-about-datetimecol) - for date-times (uses
  `format_datetime` from `babel.dates`).

* [`LinkCol`](#more-about-linkcol) - creates a link by specifying an
  endpoint and url_kwargs.

* [`ButtonCol`](#more-about-buttoncol) (subclass of LinkCol) creates a
  button that posts the the given address.

* [`NestedTableCol`](#more-about-nestedtablecol) - allows nesting of
  tables inside columns

More about `OptCol`
-------------------

When creating the column, you pass some `choices`. This should be a
dict with the keys being the values that will be found on the item's
attribute, and the values will be the text to be displayed.

You can also set a `default_key`, or a `default_value`. The default
value will be used if the value found from the item isn't in the
choices dict. The default key works in much the same way, but means
that if your default is already in your choices, you can just point to
it rather than repeat it.

And you can use `coerce_fn` if you need to alter the value from the
item before looking it up in the dict.

More about `BoolCol`
--------------------

A subclass of `OptCol` where the `choices` are:

```python
{True: 'Yes', False: 'No'}
```

and the `coerce_fn` is `bool`. So the value from the item is coerced
to a `bool` and then looked up in the choices to get the text to
display.

If you want to specify something other than "Yes" and "No", you can
pass `yes_display` and/or `no_display` when creating the column. Eg:

```python
class MyTable(Table):
    mybool = BoolCol('myboolcol', yes_display='Affirmative', no_display='Negatory')
```

More about `BoolNaCol`
----------------------

Just like `BoolCol`, except displays `None` as "N/A". Can override
with the `na_display` argument.

More about `DateCol`
--------------------

[Requires Babel configuration](#babel-configuration)

Formats a date from the item. Can specify a `date_format` to use,
which defaults to `'short'`, which is passed to
`babel.dates.format_date`.

More about `DatetimeCol`
------------------------

[Requires Babel configuration](#babel-configuration)

Formats a datetime from the item. Can specify a `datetime_format` to
use, which defaults to `'short'`, which is passed to
`babel.dates.format_datetime`.

Babel configuration
-------------------

Babel uses a locale to determine how to format dates. It falls back to
using environment variables (`LC_TIME`, `LANGUAGE`, `LC_ALL`,
`LC_CTYPE`, `LANG`), or can be configured
[within Flask](https://pythonhosted.org/Flask-Babel/#configuration),
allowing dynamic selection of locale.

Make sure that one of the following is true:

- at least one of the above environment variables is set to a valid locale
- `BABEL_DEFAULT_LOCALE` is set as config on the Flask app to a valid locale
- a `@babel.localeselector` function is configured

Note that Babel reads the environment variables at import time, so if
you set these within Python, make sure it happens before you import
Flask Table. The other two options would be considered "better",
largely for this reason.

More about `LinkCol`
--------------------

Gives a way of putting a link into a `td`. You must specify an
`endpoint` for the url. You should also specify some
`url_kwargs`. This should be a dict which will be passed as the second
argument of `url_for`, except the values will be treated as attributes
to be looked up on the item. These keys obey the same rules as
elsewhere, so can be things like `'category.name'` or `('category',
'name')`.

The kwarg `url_kwargs_extra` allows passing of contants to the
url. This can be useful for adding constant GET params to a url.

The text for the link is acquired in *almost* the same way as with
other columns. However, other columns can be given no `attr` or
`attr_list` and will use the attribute that the column was given in
the table class, but `LinkCol` does not, and instead falls back to the
heading of the column. This make more sense for things like an "Edit"
link. You can override this fallback with the `text_fallback` kwarg.

Set attributes for anchor tag by passing `anchor_attrs`:
```python
name = LinkCol('Name', 'single_item', url_kwargs=dict(id='id'), anchor_attrs={'class': 'myclass'})
```

More about `ButtonCol`
----------------------

Has all the same options as `LinkCol` but instead adds a form and a
button that gets posted to the url.

You can pass a dict of attributes to add to the button element with
the `button_attrs` kwarg.

You can pass a dict of attributes to add to the form element with
the `form_attrs` kwarg.

You can pass a dict of hidden fields to add into the form element with
the `form_hidden_fields` kwargs. The keys will be used as the `name`
attributes and the values as the `value` attributes.

More about `NestedTableCol`
---------------------------

This column type makes it possible to nest tables in columns. For each
nested table column you need to define a subclass of Table as you
normally would when defining a table. The name of that Table sub-class
is the second argument to NestedTableCol.

Eg:

```python
class MySubTable(Table):
    a = Col('1st nested table col')
    b = Col('2nd nested table col')

class MainTable(Table):
    id = Col('id')
    objects = NestedTableCol('objects', MySubTable)
```

Subclassing Col
===============

(Look in examples/subclassing.py for a more concrete example)

Suppose our item has an attribute, but we don't want to output the
value directly, we need to alter it first. If the value that we get
from the item gives us all the information we need, then we can just
override the td_format method:

```python
class LangCol(Col):
    def td_format(self, content):
        if content == 'en_GB':
            return 'British English'
        elif content == 'de_DE':
            return 'German'
        elif content == 'fr_FR':
            return 'French'
        else:
            return 'Not Specified'
```

If you need access to all of information in the item, then we can go a
stage earlier in the process and override the td_contents method:

```python
from flask import Markup

def td_contents(self, i, attr_list):
    # by default this does
    # return self.td_format(self.from_attr_list(i, attr_list))
    return Markup.escape(self.from_attr_list(i, attr_list) + ' for ' + item.name)
```

At present, you do still need to be careful about escaping things as
you override these methods. Also, because of the way that the Markup
class works, you need to be careful about how you concatenate these
with other strings.

Manipulating `<tr>`s
====================

(Look in examples/rows.py for a more concrete example)

Suppose you want to change something about the tr element for some or
all items. You can do this by overriding your table's `get_tr_attrs`
method. By default, this method returns an empty dict.

So, we might want to use something like:

```python
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')

    def get_tr_attrs(self, item):
        if item.important():
            return {'class': 'important'}
        else:
            return {}
```

which would give all trs for items that returned a true value for the
`important()` method, a class of "important".

Dynamically Creating Tables
===========================

(Look in examples/dynamic.py for a more concrete example)

You can define a table dynamically too.

```python
TableCls = create_table('TableCls')\
    .add_column('name', Col('Name'))\
    .add_column('description', Col('Description'))
```

which is equivalent to

```python
class TableCls(Table):
    name = Col('Name')
    description = Col('Description')
```

but makes it easier to add columns dynamically.

For example, you may wish to only add a column based on a condition.

```python
TableCls = create_table('TableCls')\
    .add_column('name', Col('Name'))

if condition:
    TableCls.add_column('description', Col('Description'))
```

which is equivalent to

```python
class TableCls(Table):
    name = Col('Name')
    description = Col('Description', show=condition)
```

thanks to the `show` option. Use whichever you think makes your code
more readable. Though you may still need the dynamic option for
something like

```python
TableCls = create_table('TableCls')
for i in range(num):
    TableCls.add_column(str(i), Col(str(i)))
```

We can also set some extra options to the table class by passing `options` parameter to `create_table()`:
```python
tbl_options = dict(
    classes=['cls1', 'cls2'],
    thead_classes=['cls_head1', 'cls_head2'],
    no_items='Empty')
TableCls = create_table(options=tbl_options)

# equals to

class TableCls(Table):
    classes = ['cls1', 'cls2']
    thead_classes = ['cls_head1', 'cls_head2']
    no_items = 'Empty'
```

Sortable Tables
===============

(Look in examples/sortable.py for a more concrete example)

Define a table and set its allow_sort attribute to True. Now all
columns will be default try to turn their header into a link for
sorting, unless you set allow_sort to False for a column.

You also must declare a sort_url method for that table. Given a
col_key, this determines the url for link in the header. If reverse is
True, then that means that the table has just been sorted by that
column and the url can adjust accordingly, ie to now give the address
for the table sorted in the reverse direction. It is, however,
entirely up to your flask view method to interpret the values given to
it from this url and to order the results before giving the to the
table. The table itself will not do any reordering of the items it is
given.

```python
class SortableTable(Table):
    name = Col('Name')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction =  'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)
```

The Examples
============

The [`examples`](/examples) directory contains a few pieces of sample code to show
some of the concepts and features. They are all intended to be
runnable. Some of them just output the code they generate, but some
(just one, `sortable.py`, at present) actually creates a Flask app
that you can access.

You should be able to just run them directly with `python`, but if you
have cloned the repository for the sake of dev, and created a
virtualenv, you may find that they generate an import error for
`flask_table`. This is because `flask_table` hasn't been installed,
and can be rectified by running something like
`PYTHONPATH=.:./lib/python3.3/site-packages python examples/simple.py`,
which will use the local version of `flask_table`
including any changes.

Also, if there is anything that you think is not clear and would be
helped by an example, please just ask and I'll happily write one. Only
you can help me realise which bits are tricky or non-obvious and help
me to work on explaining the bits that need explaining.

Other Things
============

At the time of first writing, I was not aware of the work of
Django-Tables. However, I have now found it and started adapting ideas
from it, where appropriate. For example, allowing items to be dicts as
well as objects.

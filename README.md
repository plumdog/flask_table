Flask Table
===========

Because writing HTML is fiddly and all of your tables are basically
the same.

[![Build Status](https://travis-ci.org/plumdog/flask_table.svg?branch=master)](https://travis-ci.org/plumdog/flask_table)

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

Extra things:
-------------

* The attribute used for each column in the declaration of the column
  is used as the default thing to lookup in each item.

* The thing that you pass when you populate the table must:
  * be iterable
  * contain dicts or objects - there's nothing saying it can't contain
    some of each

* There are also LinkCol and ButtonCol that allow links and buttons,
  which is where the Flask-specific-ness comes in.

* There are also DateCol and DatetimeCol that format dates and
  datetimes.

* Oh, and BoolCol, which does Yes/No.

* But most importantly, Col is easy to subclass.

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

The `examples` directory contains a few pieces of sample code to show
some of the concepts and features. They are all intended to be
runnable. Some of them just output the code they generate, but some
(just one, `sortable.py`, at present) actually creates a Flask app
that you can access.

You should be able to just run them directly with `python`, but if you
have cloned the repository for the sake of dev, and created a
virtualenv, you may find that they generate an import error for
`flask_table`. This is because `flask_table` hasn't been installed,
and can be rectified by running something like
`PYTHONPATH=$PYTHONPATH:. python examples/simple.py`.

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

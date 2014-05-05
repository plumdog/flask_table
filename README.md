Flask Table
===========

Because writing HTML is fiddly and all of your tables are basically
the same.

Quick Start
===========

```python
# import things
from flask_table import Table, Col

# Declare your table
class MyTable(Table):
    name = Col('Name')
    description = Col('Description')

# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
items = [Item('Name1', 'Desc1'), Item('Name2', 'Desc2')]
# Or, equivalently, some dicts
items = [dict(name='Name1', description='Desc1'),
         dict(name='Name2', description='Desc2')]
# Or, more likely, something like
items = Item.query.all()

# Populate the table
table = MyTable(items)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template
```

Extra things:
-------------

* The attribute used for each column in the declaration of the column
  is used as the default thing to lookup in each item.

* The thing that you pass when you populate the table must:
  * be iterable
  * be len()-able
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

Other Things
============

At the time of first writing, I was not aware of the work of
Django-Tables. However, I have now found it and started adapting ideas
from it, where appropriate. For example, allowing items to be dicts as
well as objects.

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

# Populate the table
table = MyTable(items)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template
```

Extra things:

* The attribute used for each column in the declaration of the column
  is used as the default thing to lookup in each object.

* There are also LinkCol and ButtonCol that allow links and buttons,
  which is where the Flask-specific-ness comes in.

* There are also DateCol and DatetimeCol that format dates and
  datetimes.

* Oh, and BoolCol, which does Yes/No.

* But most importantly, Col is easy to subclass.

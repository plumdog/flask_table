import os
from datetime import datetime

# Run this example with LC_TIME=[other locale] to use a different
# locale's datetime formatting, eg:
#
# LC_TIME=en_US python examples/datetimecol.py
# or
# LC_TIME=en_GB python examples/datetimecol.py
os.environ.setdefault('LC_TIME', 'en_GB')  # noqa

from flask_table import Table, Col, DatetimeCol


class Item(object):
    def __init__(self, name, dt):
        self.name = name
        self.dt = dt


class ItemTable(Table):
    name = Col('Name')
    dt = DatetimeCol('Datetime')


def main():
    items = [
        Item('Name1', datetime.now()),
        Item('Name2', datetime(2018, 1, 1, 12, 34, 56)),
    ]

    table = ItemTable(items)

    # or {{ table }} in jinja
    print(table.__html__())

if __name__ == '__main__':
    main()

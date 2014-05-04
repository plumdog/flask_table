import os
import unittest

from bs4 import BeautifulSoup

from flask import Flask
from flask_table import Table, Col, LinkCol, ButtonCol
import flask.ext.testing as flask_testing

class Item(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class Subitem(Item):
    pass


class TableTest(unittest.TestCase):
    def assert_in(self, x, y):
        if x not in y:
            raise AssertionError('%s is not in %s, but should be.' % (x, y))

    def assert_in_html(self, x, y):
        return self.assert_in(x, y.__html__())

    def assert_not_in(self, x, y):
        if x in y:
            raise AssertionError('%s is in %s, but shouldn\'t be.' % (x, y))

    def assert_not_in_html(self, x, y):
        return self.assert_not_in(x, y.__html__())

    def assert_html_equivalent(self, test_tab, reference):
        x_beaut = BeautifulSoup(test_tab.__html__()).prettify(formatter=None).strip()
        y_beaut = BeautifulSoup(reference).prettify(formatter=None).strip()
        self.assertEqual(x_beaut, y_beaut)

    @classmethod
    def get_html(cls, d, name):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'html', d, name + '.html')
        with open(path) as f:
            return str(f.read())

    def assert_html_equivalent_from_file(self, d, name, items, print_html=False):
        tab = self.table_cls(items)
        if print_html:
            print(tab.__html__())
        html = self.get_html(d, name)
        self.assert_html_equivalent(tab, html)


def test_app():
    app = Flask(__name__)

    @app.route('/view/<int:id_>')
    def view(id_):
        return 'View %s' % id_

    @app.route('/delete/<int:id_>', methods=['POST'])
    def delete(id_):
        return 'Delete %s' % id_

    return app


class FlaskTableTest(flask_testing.TestCase, TableTest):
    def create_app(self):
        return test_app()


class ColTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file('col_test', 'test_one', items)

    def test_two(self):
        items = [Item(name='one'), Item(name='two')]
        self.assert_html_equivalent_from_file('col_test', 'test_two', items)

    def test_ten(self):
        items = [Item(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file('col_test', 'test_ten', items)


class AttrListTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Subitem Name Heading', attr_list=['subitem', 'name'])
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(subitem=Subitem(name='one'))]
        self.assert_html_equivalent_from_file('attr_list_test', 'test_one', items)

    def test_two_one_empty(self):
        items = [Item(subitem=Subitem(name='one')), Item(subitem=None)]
        self.assert_html_equivalent_from_file('attr_list_test', 'test_two_one_empty', items)


class LinkTest(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_='id'))
        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file('link_test', 'test_one', items)


class ButtonTest(FlaskTableTest):
    def setUp(self):
        class ButtonTable(Table):
            name = Col('Name')
            view = ButtonCol('Delete', 'delete', url_kwargs=dict(id_='id'))
        self.table_cls = ButtonTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file('button_test', 'test_one', items)


if __name__ == '__main__':
    main()

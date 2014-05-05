import os
import unittest

from flask import Flask
from flask_table import (Table, Col, LinkCol, ButtonCol, OptCol, BoolCol,
                         DateCol, DatetimeCol)
import flask.ext.testing as flask_testing
from datetime import date, datetime


class Item(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Subitem(Item):
    pass


def html_equivalent(a, b):
    return html_reduce(a) == html_reduce(b)


def html_reduce(s):
    return ''.join(l.strip() for l in s.split('\n'))


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
        self.assertTrue(html_equivalent(test_tab.__html__(), reference))

    @classmethod
    def get_html(cls, d, name):
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'html', d, name + '.html')
        with open(path) as f:
            return str(f.read())

    def assert_html_equivalent_from_file(self, d, name, items=[], **kwargs):
        tab = kwargs.get('tab', self.table_cls(items))
        if kwargs.get('print_html'):
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


class EmptyTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')
        self.table_cls = MyTable

    def test_none(self):
        items = []
        self.assert_html_equivalent_from_file('empty_test', 'test_none', items)


class ColDictTest(ColTest):
    def test_one(self):
        items = [dict(name='one')]
        self.assert_html_equivalent_from_file('col_test', 'test_one', items)

    def test_two(self):
        items = [dict(name='one'), dict(name='two')]
        self.assert_html_equivalent_from_file('col_test', 'test_two', items)

    def test_ten(self):
        items = [dict(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file('col_test', 'test_ten', items)


class FuncItem(Item):
        def get_name(self):
            return self.name


class ColCallableTest(ColTest):
    def setUp(self):
        class MyTable(Table):
            get_name = Col('Name Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [FuncItem(name='one')]
        self.assert_html_equivalent_from_file('col_test', 'test_one', items)

    def test_two(self):
        items = [FuncItem(name='one'), FuncItem(name='two')]
        self.assert_html_equivalent_from_file('col_test', 'test_two', items)

    def test_ten(self):
        items = [FuncItem(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file('col_test', 'test_ten', items)


class AttrListTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Subitem Name Heading', attr_list=['subitem', 'name'])
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(subitem=Subitem(name='one'))]
        self.assert_html_equivalent_from_file(
            'attr_list_test', 'test_one', items)

    def test_two_one_empty(self):
        items = [Item(subitem=Subitem(name='one')), Item(subitem=None)]
        self.assert_html_equivalent_from_file(
            'attr_list_test', 'test_two_one_empty', items)


class WeirdAttrListTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Subitem Name Heading', attr_list=['subi.tem.', '.nam.e'])
        self.table_cls = MyTable

    def test_one(self):
        items = [{'subi.tem.': {'.nam.e': 'one'}}]
        self.assert_html_equivalent_from_file(
            'attr_list_test', 'test_one', items)


class AltAttrTest(ColTest):
    def setUp(self):
        class MyTable(Table):
            alt_name = Col('Name Heading', attr='name')
        self.table_cls = MyTable


class AttrListDotsTest(AttrListTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Subitem Name Heading', attr='subitem.name')
        self.table_cls = MyTable


class ClassTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            classes = ['table']
            name = Col('Name Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file('class_test', 'test_one', items)


class ClassTestAtPopulate(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        tab = self.table_cls(items, classes=['table'])
        self.assert_html_equivalent_from_file(
            'class_test', 'test_one', tab=tab)


class LinkTest(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_='id'))
        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file('link_test', 'test_one', items)


class LinkDictTest(LinkTest):
    def test_one(self):
        items = [dict(name='one', id=1)]
        self.assert_html_equivalent_from_file('link_test', 'test_one', items)


class LinkTestSubItemAttrList(LinkTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_=['subitem', 'id']))
        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', subitem=Subitem(id=1))]
        self.assert_html_equivalent_from_file('link_test', 'test_one', items)


class LinkTestSubItemAttrDots(LinkTestSubItemAttrList):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_='subitem.id'))
        self.table_cls = LinkTable


class ButtonTest(FlaskTableTest):
    def setUp(self):
        class ButtonTable(Table):
            name = Col('Name')
            view = ButtonCol('Delete', 'delete', url_kwargs=dict(id_='id'))
        self.table_cls = ButtonTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file('button_test', 'test_one', items)


class BoolTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            yesno = BoolCol('YesNo Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(yesno=True),
                 Item(yesno='Truthy'),
                 Item(yesno='')]
        self.assert_html_equivalent_from_file('bool_test', 'test_one', items)


class OptTest(TableTest):
    def setUp(self):
        choices = {'a': 'A', 'b': 'Bbb', 'c': 'Ccccc'}
        class MyTable(Table):
            choice = OptCol('Choice Heading', choices=choices)
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(choice='a'),
                 Item(choice='b'),
                 Item(choice='c'),
                 Item(choice='d')]
        self.assert_html_equivalent_from_file('opt_test', 'test_one', items)


class OptTestDefaultKey(TableTest):
    def setUp(self):
        choices = {'a': 'A', 'b': 'Bbb', 'c': 'Ccccc'}
        class MyTable(Table):
            choice = OptCol('Choice Heading', choices=choices, default_key='c')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(choice='a'),
                 Item(choice='b'),
                 Item(choice='c'),
                 Item(choice='d')]
        self.assert_html_equivalent_from_file('opt_test', 'test_one_default_key', items)

class OptTestDefaultValue(TableTest):
    def setUp(self):
        choices = {'a': 'A', 'b': 'Bbb', 'c': 'Ccccc'}
        class MyTable(Table):
            choice = OptCol('Choice Heading', choices=choices, default_value='Ddddddd')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(choice='a'),
                 Item(choice='b'),
                 Item(choice='c'),
                 Item(choice='d')]
        self.assert_html_equivalent_from_file('opt_test', 'test_one_default_value', items)

class DateTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            date = DateCol('Date Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(date=date(2014, 1, 1)), Item(date=None)]
        self.assert_html_equivalent_from_file('date_test', 'test_one', items)


class DatetimeTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            datetime = DatetimeCol('DateTime Heading')
        self.table_cls = MyTable

    def test_one(self):
        items = [Item(datetime=datetime(2014, 1, 1, 10, 20, 30)), Item(datetime=None)]
        self.assert_html_equivalent_from_file('datetime_test', 'test_one', items)


class EscapeTest(TableTest):
    def setUp(self):
        class EscapeTable(Table):
            name = Col('Name')
        self.table_cls = EscapeTable

    def test_one(self):
        items = [Item(name='<&"\'')]
        self.assert_html_equivalent_from_file('escape_test', 'test_one', items)

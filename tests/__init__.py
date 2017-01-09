# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
# Set all of our environment variables before we import other things
# that may read these at import time. We also use noqa to stop pep8
# from worrying about imports not being at the top of the file.
for name in ['LANGUAGE', 'LC_ALL', 'LC_CTYPE', 'LC_MESSAGES', 'LC_TIME']:  # noqa
    os.environ[name] = ''
os.environ['LANGUAGE'] = 'en_GB.UTF-8'  # noqa

import io
import unittest
from flask import Flask, url_for
from flask_table import (Table, Col, LinkCol, ButtonCol, OptCol, BoolCol,
                         DateCol, DatetimeCol, NestedTableCol, create_table)
import flask.ext.testing as flask_testing
from datetime import date, datetime


class Item(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Subitem(Item):
    pass


def html_reduce(s):
    return ''.join(l.strip() for l in s.split('\n'))


class TableTest(unittest.TestCase):
    def assert_in(self, x, y):
        if x not in y:
            raise AssertionError(
                '{x} is not in {y}, but should be.'.format(x=x, y=y))

    def assert_in_html(self, x, y):
        return self.assert_in(x, y.__html__())

    def assert_not_in(self, x, y):
        if x in y:
            raise AssertionError(
                '{x} is in {y}, but shouldn\'t be.'.format(x=x, y=y))

    def assert_not_in_html(self, x, y):
        return self.assert_not_in(x, y.__html__())

    def assert_html_equivalent(self, test_tab, reference):
        self.assertEqual(
            html_reduce(test_tab.__html__()),
            html_reduce(reference))

    @classmethod
    def get_html(cls, d, name):
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'html', d, name + '.html')
        with io.open(path, encoding="utf8") as f:
            return f.read()

    def assert_html_equivalent_from_file(self, d, name, items=[], **kwargs):
        table_id = kwargs.get('table_id', None)
        border = kwargs.get('border', False)
        tab = kwargs.get('tab', self.table_cls(
            items, table_id=table_id, border=border))
        if kwargs.get('print_html'):
            print(tab.__html__())
        html = self.get_html(d, name)
        self.assert_html_equivalent(tab, html)


def test_app():
    app = Flask(__name__)

    @app.route('/', defaults=dict(sort=None, direction=None))
    @app.route('/sort/<string:sort>/', defaults=dict(direction=None))
    @app.route('/sort/<string:sort>/direction/<string:direction>/')
    def index(sort, direction):
        return 'Index'

    @app.route('/view/<int:id_>')
    def view(id_):
        return 'View {}'.format(id_)

    @app.route('/delete/<int:id_>', methods=['POST'])
    def delete(id_):
        return 'Delete {}'.format(id_)

    return app


class FlaskTableTest(flask_testing.TestCase, TableTest):
    def create_app(self):
        return test_app()


class TableIDTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file(
            'tableid_test', 'test_one', items, table_id='Test table ID')


class BorderTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name')
            description = Col('Description')
        self.table_cls = MyTable

        self.items = [Item(name='Name1', description='Description1'),
                      Item(name='Name2', description='Description2'),
                      Item(name='Name3', description='Description3')]

    def test_one(self):
        self.assert_html_equivalent_from_file(
            'border_test', 'table_bordered', self.items, border=True)

    def test_two(self):
        table_bordered = self.table_cls(self.items, border=True)
        self.assert_html_equivalent_from_file(
            'border_test', 'table_bordered', tab=table_bordered)


class ColTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_one', items)

    def test_two(self):
        items = [Item(name='one'), Item(name='two')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_two', items)

    def test_ten(self):
        items = [Item(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_ten', items)

    def test_encoding(self):
        items = [Item(name='äöüß')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_encoding', items)


class HideTest(ColTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')
            hidden = Col('Hidden', show=False)

        self.table_cls = MyTable


class DynamicColsTest(ColTest):
    def setUp(self):
        self.table_cls = create_table().add_column('name', Col('Name Heading'))


class DynamicColsNumColsTest(TableTest):
    def setUp(self):
        self.table_cls = create_table()
        for i in range(3):
            self.table_cls.add_column(str(i), Col(str(i)))

    def test_one(self):
        items = [{str(i): i for i in range(3)}]
        self.assert_html_equivalent_from_file(
            'dynamic_cols_num_cols_test', 'test_one', items)

    def test_ten(self):
        items = [{str(i): i for i in range(3)}] * 10
        self.assert_html_equivalent_from_file(
            'dynamic_cols_num_cols_test', 'test_ten', items)


class DynamicColsInheritTest(TableTest):
    def setUp(self):
        # Start with MyTable
        class MyTable(Table):
            name = Col('Name')

        # Then dynamically extend it.
        self.table_cls = create_table(base=MyTable)
        self.table_cls.add_column('number', Col('Number'))

    def test_one(self):
        items = [{'name': 'TestName', 'number': 10}]
        self.assert_html_equivalent_from_file(
            'dynamic_cols_inherit_test', 'test_one', items)


class DynamicColsOptionsTest(TableTest):
    def setUp(self):
        tbl_options = dict(
            classes=['cls1', 'cls2'],
            thead_classes=['cls_head1', 'cls_head2'],
            no_items='Empty')
        self.table_cls = create_table(options=tbl_options)
        self.table_cls.add_column('name', Col('Name Heading'))

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file(
            'dynamic_cols_options_test', 'test_one', items)

    def test_none(self):
        items = []
        self.assert_html_equivalent_from_file(
            'dynamic_cols_options_test', 'test_none', items)


class OverrideTrTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            number = Col('Number')

            def get_tr_attrs(self, item):
                if item['number'] % 3 == 1:
                    return {'class': 'threes-plus-one'}
                elif item['number'] % 3 == 2:
                    return {'class': 'threes-plus-two'}
                return {}

        self.table_cls = MyTable

    def test_ten(self):
        items = [{'number': i} for i in range(10)]
        self.assert_html_equivalent_from_file(
            'override_tr_test', 'test_ten', items)


class EmptyTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_none(self):
        items = []
        self.assert_html_equivalent_from_file(
            'empty_test', 'test_none', items)


class ColDictTest(ColTest):
    def test_one(self):
        items = [dict(name='one')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_one', items)

    def test_two(self):
        items = [dict(name='one'), dict(name='two')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_two', items)

    def test_ten(self):
        items = [dict(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_ten', items)

    def test_encoding(self):
        items = [dict(name='äöüß')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_encoding', items)


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
        self.assert_html_equivalent_from_file(
            'col_test', 'test_one', items)

    def test_two(self):
        items = [FuncItem(name='one'), FuncItem(name='two')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_two', items)

    def test_ten(self):
        items = [FuncItem(name=str(i)) for i in range(10)]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_ten', items)

    def test_encoding(self):
        items = [FuncItem(name='äöüß')]
        self.assert_html_equivalent_from_file(
            'col_test', 'test_encoding', items)


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
            name = Col(
                'Subitem Name Heading', attr_list=['subi.tem.', '.nam.e'])

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
        self.assert_html_equivalent_from_file(
            'class_test', 'test_one', items)


class TheadClassTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            thead_classes = ['table-head']
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file(
            'thead_class_test', 'test_one', items)


class SortUrlNotSetTest(TableTest):
    def setUp(self):
        class MyTable1(Table):
            allow_sort = True
            name = Col('Name Heading')

        self.table_cls1 = MyTable1

        class MyTable2(Table):
            allow_sort = True
            name = Col('Name Heading')

            def sort_url(self, col_id, reverse=False):
                return '?sort={}&reverse={}'.format(col_id, reverse)

        self.table_cls2 = MyTable2

    def test_fail(self):
        items = [{'name': 'TestName'}]

        def _create_table1():
            html = self.table_cls1(items, sort_by='name').__html__()

        def _create_table2():
            html = self.table_cls2(items, sort_by='name').__html__()

        # table1 should raise a NotImplementedError
        self.assertRaises(NotImplementedError, _create_table1)
        # table2 should work fine
        try:
            _create_table2()
        except Exception:
            self.fail('Table creation failed unexpectedly')


class NoItemsTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            no_items = 'There is nothing here'
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_zero(self):
        items = []
        self.assert_html_equivalent_from_file(
            'no_items_test', 'test_zero', items)


class NoItemsDynamicTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_zero(self):
        items = []
        tab = self.table_cls(items, no_items='There is nothing here')
        self.assert_html_equivalent_from_file(
            'no_items_test', 'test_zero', tab=tab)


class NoItemsAllowEmptyTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')
            allow_empty = True

        self.table_cls = MyTable

    def test_zero(self):
        items = []
        self.assert_html_equivalent_from_file(
            'no_items_allow_empty', 'test_zero', items)


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


class TheadClassTestAtPopulate(TableTest):
    def setUp(self):
        class MyTable(Table):
            name = Col('Name Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(name='one')]
        tab = self.table_cls(items, thead_classes=['table-head'])
        self.assert_html_equivalent_from_file(
            'thead_class_test', 'test_one', tab=tab)


class LinkTest(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_='id'))

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one', items)


class LinkExtraKwargsTest(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol(
                'View',
                'view',
                url_kwargs=dict(id_='id'),
                url_kwargs_extra=dict(extra='extra'))

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one_extra_kwargs', items)


class LinkExtraKwargsRepeatTest(FlaskTableTest):
    """Check that if both `url_kwargs` and `url_kwargs_extra` are given
    and share a key that we default to the value from the item, rather
    than the static value from `url_kwargs_extra`.

    """
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol(
                'View',
                'view',
                url_kwargs=dict(id_='id'),
                url_kwargs_extra=dict(id_='id-from-extra', extra='extra'))

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one_extra_kwargs', items)


class LinkDictTest(LinkTest):
    def test_one(self):
        items = [dict(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one', items)


class LinkNoUrlKwargsTest(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'index')

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one')]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one_no_url_kwargs', items)


class LinkTestSubItemAttrList(LinkTest):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol(
                'View', 'view', url_kwargs=dict(id_=['subitem', 'id']))

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', subitem=Subitem(id=1))]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one', items)


class LinkTestSubItemAttrDots(LinkTestSubItemAttrList):
    def setUp(self):
        class LinkTable(Table):
            name = Col('Name')
            view = LinkCol('View', 'view', url_kwargs=dict(id_='subitem.id'))

        self.table_cls = LinkTable


class LinkTestCustomContent(FlaskTableTest):
    def setUp(self):
        class LinkTable(Table):
            name = LinkCol(
                'View', 'view', attr='name', url_kwargs=dict(id_='id'))

        self.table_cls = LinkTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'link_test', 'test_one_custom_content', items)


class ButtonTest(FlaskTableTest):
    def setUp(self):
        class ButtonTable(Table):
            name = Col('Name')
            view = ButtonCol('Delete', 'delete', url_kwargs=dict(id_='id'))

        self.table_cls = ButtonTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'button_test', 'test_one', items)


class ButtonAttrsTest(FlaskTableTest):
    def setUp(self):
        class ButtonTable(Table):
            name = Col('Name')
            view = ButtonCol(
                'Delete',
                'delete',
                url_kwargs=dict(id_='id'),
                button_attrs={'class': 'myclass'})
        self.table_cls = ButtonTable

    def test_one(self):
        items = [Item(name='one', id=1)]
        self.assert_html_equivalent_from_file(
            'button_attrs_test', 'test_one', items)


class BoolTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            yesno = BoolCol('YesNo Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(yesno=True),
                 Item(yesno='Truthy'),
                 Item(yesno='')]
        self.assert_html_equivalent_from_file(
            'bool_test', 'test_one', items)


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
        self.assert_html_equivalent_from_file(
            'opt_test', 'test_one', items)


class OptNoChoicesTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            choice = OptCol('Choice Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(choice='a')]
        self.assert_html_equivalent_from_file(
            'opt_test', 'test_one_no_choices', items)


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
        self.assert_html_equivalent_from_file(
            'opt_test', 'test_one_default_key', items)


class OptTestDefaultValue(TableTest):
    def setUp(self):
        choices = {'a': 'A', 'b': 'Bbb', 'c': 'Ccccc'}

        class MyTable(Table):
            choice = OptCol(
                'Choice Heading', choices=choices, default_value='Ddddddd')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(choice='a'),
                 Item(choice='b'),
                 Item(choice='c'),
                 Item(choice='d')]
        self.assert_html_equivalent_from_file(
            'opt_test', 'test_one_default_value', items)


class DateTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            date = DateCol('Date Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(date=date(2014, 1, 1)), Item(date=None)]
        self.assert_html_equivalent_from_file(
            'date_test', 'test_one', items)


class DateTestFormat(TableTest):
    def setUp(self):
        class MyTable(Table):
            date = DateCol('Date Heading', date_format="YYYY-MM-dd")

        self.table_cls = MyTable

    def test_one(self):
        items = [Item(date=date(2014, 2, 1)), Item(date=None)]
        self.assert_html_equivalent_from_file(
            'date_test_format', 'test_one', items)


class DatetimeTest(TableTest):
    def setUp(self):
        class MyTable(Table):
            datetime = DatetimeCol('DateTime Heading')

        self.table_cls = MyTable

    def test_one(self):
        items = [
            Item(datetime=datetime(2014, 1, 1, 10, 20, 30)),
            Item(datetime=None)]
        self.assert_html_equivalent_from_file(
            'datetime_test', 'test_one', items)


class DatetimeTestFormat(TableTest):
    def setUp(self):
        class MyTable(Table):
            datetime = DatetimeCol(
                'DateTime Heading',
                datetime_format="YYYY-MM-dd hh:mm")

        self.table_cls = MyTable

    def test_one(self):
        items = [
            Item(datetime=datetime(2014, 1, 1, 10, 20, 30)),
            Item(datetime=None)]
        self.assert_html_equivalent_from_file(
            'datetime_test_format', 'test_one', items)


class EscapeTest(TableTest):
    def setUp(self):
        class EscapeTable(Table):
            name = Col('Name')

        self.table_cls = EscapeTable

    def test_one(self):
        items = [Item(name='<&"\'')]
        self.assert_html_equivalent_from_file(
            'escape_test', 'test_one', items)


class SortingTest(FlaskTableTest):
    def setUp(self):
        class SortingTable(Table):
            allow_sort = True
            name = Col('Name')

            def sort_url(self, col_key, reverse=False):
                kwargs = {'sort': col_key}
                if reverse:
                    kwargs['direction'] = 'desc'
                return url_for('index', **kwargs)

        self.table_cls = SortingTable

    def test_start(self):
        items = [Item(name='name')]
        self.assert_html_equivalent_from_file(
            'sorting_test', 'test_start', items)

    def test_sorted(self):
        items = [Item(name='name')]
        tab = self.table_cls(items, sort_by='name')
        self.assert_html_equivalent_from_file(
            'sorting_test', 'test_sorted', items, tab=tab)

    def test_sorted_reverse(self):
        items = [Item(name='name')]
        tab = self.table_cls(items, sort_by='name', sort_reverse=True)
        self.assert_html_equivalent_from_file(
            'sorting_test', 'test_sorted_reverse', items, tab=tab)


class GeneratorTest(TableTest):
    def setUp(self):

        class GeneratorTable(Table):
            number = Col('Number')

        self.table_cls = GeneratorTable

        def gen_nums(upto):
            i = 1
            while True:
                if i > upto:
                    return
                yield {'number': i}
                i += 1

        self.gen_nums = gen_nums

    def test_one(self):
        items = self.gen_nums(1)
        self.assert_html_equivalent_from_file(
            'generator_test', 'test_one', items)

    def test_empty(self):
        items = self.gen_nums(0)
        self.assert_html_equivalent_from_file(
            'generator_test', 'test_empty', items)

    def test_ten(self):
        items = self.gen_nums(10)
        self.assert_html_equivalent_from_file(
            'generator_test', 'test_ten', items)


class NestedColTest(TableTest):
    def setUp(self):
        class MySubTable(Table):
            b = Col('b')
            c = Col('c')

        class MyMainTable(Table):
            a = Col('a')
            nest = NestedTableCol('Nested column', MySubTable)

        self.table_cls = MyMainTable

    def test_one(self):
        items = [Item(a='row1', nest=[Item(b='r1asc1', c='r1asc2'),
                                      Item(b='r1bsc1', c='r1bsc2')]),
                 Item(a='row2', nest=[Item(b='r2asc1', c='r2asc2'),
                                      Item(b='r2bsc1', c='r2bsc2')])]
        self.assert_html_equivalent_from_file(
            'nestedcol_test', 'test_one', items)

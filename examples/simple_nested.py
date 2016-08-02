from flask_table import Table, Col, NestedTableCol


"""Lets suppose that we have a class that we get an iterable of from
somewhere, such as a database. We can declare a table that pulls out
the relevant entries, escapes them and displays them. Additionally,
we show here how to used a NestedTableCol, by first defining a
sub-table.

"""


class SubItem(object):
    def __init__(self, col1, col2):
        self.col1 = col1
        self.col2 = col2


class Item(object):
    def __init__(self, name, description, subtable):
        self.name = name
        self.description = description
        self.subtable = subtable


class SubItemTable(Table):
    col1 = Col('Sub-column 1')
    col2 = Col('Sub-column 2')


class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')
    subtable = NestedTableCol('Subtable', SubItemTable)


def main():
    items = [Item('Name1', 'Description1', [SubItem('r1sr1c1', 'r1sr1c2'),
                                            SubItem('r1sr2c1', 'r1sr2c2')]),
             Item('Name2', 'Description2', [SubItem('r2sr1c1', 'r2sr1c2'),
                                            SubItem('r2sr2c1', 'r2sr2c2')]),
             ]

    table = ItemTable(items)

    # or {{ table }} in jinja
    print(table.__html__())

    """Outputs:

    <table>
      <thead>
        <tr><th>Name</th><th>Description</th><th>Subtable</th></tr>
      </thead>
      <tbody>
        <tr><td>Name1</td><td>Description1</td><td><table>
              <thead>
                <tr><th>Sub-column 1</th><th>Sub-column 2</th></tr>
              </thead>
              <tbody>
                <tr><td>r1sr1c1</td><td>r1sr1c2</td></tr>
                <tr><td>r1sr2c1</td><td>r1sr2c2</td></tr>
              </tbody>
        </table></td></tr>
        <tr><td>Name2</td><td>Description2</td><td><table>
              <thead>
                <tr><th>Sub-column 1</th><th>Sub-column 2</th></tr>
              </thead>
              <tbody>
                <tr><td>r2sr1c1</td><td>r2sr1c2</td></tr>
                <tr><td>r2sr2c1</td><td>r2sr2c2</td></tr>
              </tbody>
        </table></td></tr>
      </tbody>
    </table>

    Except it doesn't bother to prettify the output.
    """

if __name__ == '__main__':
    main()

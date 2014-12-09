from flask_table import Table, Col


"""Lets suppose that we have a class that we get an iterable of from
somewhere, such as a database. We can declare a table that pulls out
the relevant entries, escapes them and displays them.

"""


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')


def main():
    items = [Item('Name1', 'Description1'),
             Item('Name2', 'Description2'),
             Item('Name3', 'Description3')]

    table = ItemTable(items)

    # or {{ table }} in jinja
    print(table.__html__())

    """Outputs:

    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name1</td>
          <td>Description1</td>
        </tr>
        <tr>
          <td>Name2</td>
          <td>Description2</td>
        </tr>
        <tr>
          <td>Name3</td>
          <td>Description3</td>
        </tr>
      </tbody>
    </table>

    Except it doesn't bother to prettify the output.
    """

if __name__ == '__main__':
    main()

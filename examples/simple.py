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
    items = [Item('A', 'aaa'),
             Item('B', 'bbb')]

    tab = ItemTable(items)

    # or {{ tab }} in jinja
    print(tab.__html__())

    """Outputs:

    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>A</td>
          <td>aaa</td>
        </tr>
        <tr>
          <td>B</td>
          <td>bbb</td>
        </tr>
      </tbody>
    </table>

    Except it doesn't bother to prettify the output.
    """

if __name__ == '__main__':
    main()

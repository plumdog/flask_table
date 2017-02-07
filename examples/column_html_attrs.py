from flask_table import Table, Col


"""What if we need to apply some classes (or any other attribute) to
the td and th HTML attributes? Maybe you want this so you can apply
some styling or attach some javascript.

NB: This example just handles the adding of some fixed attributes to a
column. If you want to do something dynamic (eg, only applying an
attribute to certain rows, see the rows.py example).

This example is not very "real world" but should show how the setting
of elements works and what things you can do.

"""


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class ItemTable(Table):
    name = Col(
        'Name',
        # Apply this class to both the th and all tds in this column
        column_html_attrs={'class': 'my-name-class'},
    )
    description = Col(
        'Description',
        # Apply these to both
        column_html_attrs={
            'data-something': 'my-data',
            'class': 'my-description-class'},
        # Apply this to just the th
        th_html_attrs={'data-something-else': 'my-description-th-class'},
        # Apply this to just the td - note that this will things from
        # overwrite column_html_attrs.
        td_html_attrs={'data-something': 'my-td-only-data'},
    )


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
          <th class="my-name-class">Name</th>
          <th class="my-description-class"
              data-something="my-data"
              data-something-else="my-description-th-class">
            Description
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="my-name-class">Name1</td>
          <td class="my-description-class"
              data-something="my-td-only-data">
            Description1
          </td>
        </tr>
        <tr>
          <td class="my-name-class">Name2</td>
          <td class="my-description-class"
              data-something="my-td-only-data">
            Description2
          </td>
        </tr>
        <tr>
          <td class="my-name-class">Name3</td>
          <td class="my-description-class"
              data-something="my-td-only-data">
            Description3
          </td>
        </tr>
      </tbody>
    </table>

    Except it doesn't bother to prettify the output.
    """

if __name__ == '__main__':
    main()

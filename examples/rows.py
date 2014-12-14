from flask_table import Table, Col


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def important(self):
        """Items are important if their description starts with an a.

        """

        return self.description.lower().startswith('a')


class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')

    def tr_format(self, item):
        if item.important():
            return '<tr class="important">{}</tr>'
        else:
            return '<tr>{}</tr>'


def main():
    items = [Item('Name1', 'Boring'),
             Item('Name2', 'A very important item'),
             Item('Name3', 'Boring')]

    table = ItemTable(items)

    print(table.__html__())

    """
    Outputs:

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
          <td>Boring</td>
        </tr>
        <tr class="important">
          <td>Name2</td>
          <td>A very important item</td>
        </tr>
        <tr>
          <td>Name3</td>
          <td>Boring</td>
        </tr>
      </tbody>
    </table>
    """


if __name__ == '__main__':
    main()

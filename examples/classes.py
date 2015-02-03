from flask_table import Table, Col


"""If we want to put an HTML class onto the table element, we can set
the "classes" attribute on the table class. This should be an iterable
of that are joined together and all added as classes. If none are set,
then no class is added to the table element.

"""


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class ItemTableOneClass(Table):
    classes = ['class1']

    name = Col('Name')
    description = Col('Description')


class ItemTableTwoClasses(Table):
    classes = ['class1', 'class2']

    name = Col('Name')
    description = Col('Description')


def one_class(items):
    table = ItemTableOneClass(items)

    # or {{ table }} in jinja
    print(table.__html__())

    """Outputs:

    <table class="class1">
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
      </tbody>
    </table>
    """


def two_classes(items):
    table = ItemTableTwoClasses(items)

    # or {{ table }} in jinja
    print(table.__html__())

    """Outputs:

    <table class="class1 class2">
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
      </tbody>
    </table>
    """


def main():
    items = [Item('Name1', 'Description1')]

    # user ItemTableOneClass
    one_class(items)

    print('\n######################\n')

    # user ItemTableTwoClasses
    two_classes(items)


if __name__ == '__main__':
    main()

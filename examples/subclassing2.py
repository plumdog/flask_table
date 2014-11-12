from flask_table import Table, Col


class RawCol(Col):
    """Class that will just output whatever it is given and will not
    escape it.
    """

    def td_format(self, content):
        return content


class ItemTable(Table):
    name = Col('Name')
    raw = RawCol('Raw')


def main():
    items = [{'name': 'A', 'raw': '<span>a</span>'},
             {'name': 'B', 'raw': '<span>b</span>'}]

    tab = ItemTable(items)

    # or {{ tab }} in jinja
    print(tab.__html__())

if __name__ == '__main__':
    main()

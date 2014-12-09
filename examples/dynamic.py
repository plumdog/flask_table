from flask_table import create_table, Col


def main():
    TableCls = create_table()\
        .add_column('name', Col('Name'))\
        .add_column('description', Col('Description'))

    items = [dict(name='Name1', description='Description1'),
             dict(name='Name2', description='Description2'),
             dict(name='Name3', description='Description3')]

    table = TableCls(items)

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
    """


if __name__ == '__main__':
    main()

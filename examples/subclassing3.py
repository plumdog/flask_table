from flask_table import Table, Col, ButtonCol
from flask import Flask, request

"""An example for creating LinkCol or ButtonCol with local attributes
   that can't be initially set when subclassing Table

"""

app = Flask(__name__)


class LocalAttributeLinkTable(Table):
    name = Col('Name')

    def __init__(self, local_attribute, items):
        super(LocalAttributeLinkTable, self).__init__(items)

        # Add a column depending on a attribute passed to
        # the constructor
        self.add_column('redirectWithLocalID',
                        ButtonCol('Select this', 'some_url',
                                  url_kwargs_extra=dict(
                                      someLocalID=local_attribute)))


@app.route('/', methods=['POST'])
def index():
    items = [{'name': 'A'},
             {'name': 'B'}]

    # This local attribute could be changed on each call to this route
    some_local_attribute = '68f36d30-6600-4a67-b2d4-7cc011ceea0e'

    # Pass some local static attribute to a table
    table = LocalAttributeLinkTable(some_local_attribute, items)

    # You would usually want to pass table out to a template with
    # render_template.
    return table.__html__()


@app.route('/some_url', methods=['POST'])
def some_url():
    local_attribute_passed = request.args.get('someLocalID')

    # Display the local attribute for testing purposes
    return '<html>local_attribute: "' + local_attribute_passed + '"</html>'


if __name__ == '__main__':
    app.run(debug=True)

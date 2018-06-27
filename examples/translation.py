from flask_table import Table, Col, ButtonCol
from flask import Flask
from flask_babelex import Babel, Domain, _

"""An example for creating LinkCol or ButtonCol with translations.
   You have to call ./babel.sh lncompile before using this example.
"""

# Setup the flask app
app = Flask(__name__)

# Setup babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en_GB'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
language_domain = Domain(dirname='translations', domain='messages')
language = Babel(default_locale='en_GB', configure_jinja=True, default_domain=language_domain)
language.init_app(app)


# This class shows how to use translations for columns and tables
class TranslatedTable(Table):
    name = Col('name')
    button = ButtonCol('button_name', 'some_url', translation_enabled=True)

    def __init__(self, items):
        super(TranslatedTable, self).__init__(items, translation_enabled=True)


# The main page
@app.route('/', methods=['GET', 'POST'])
def index():
    # The column names will be translated by flask_table
    items = [{'name': 'A'},
             {'name': 'B'}]

    # Pass some translated items to TranslatedTable
    table = TranslatedTable(items)

    # return a translated table
    return '<html>' + table.__html__() + '</html>'


# A page to redirect to
@app.route('/some_url', methods=['GET', 'POST'])
def some_url():
    # Display the local attribute for testing purposes
    return '<html>Redirected</html>'


if __name__ == '__main__':
    app.run(debug=True)

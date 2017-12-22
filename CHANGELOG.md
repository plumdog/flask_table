0.5.0
-----
- Sort out html_attrs (#80)
- Refactor test assert method (#81)
- SQLAlchemy example (#82)
- LinkCol and ButtonCol text_fallback option (#83)
- Better docs for table options (#88)
- ButtonCol form attributes (#89)
- ButtonCol form hidden fields (#90)
- Fix docs for BoolNaCol (#91)

0.4.1
-----
- Add anchor_attrs to LinkCol (#73)
- Test against more recent Python3 versions

0.4.0
-----
- Add column_html_attrs, td_html_attrs and th_html_attrs kwargs to Col (#71)

0.3.4
-----
- Remove any flask.ext imports (#69)

0.3.3
-----
- Customisable BoolCol display values (#61)
- Add BoolNaCol (#62)
- Reduce TableTest boilerplate (#63)
- Fix for deprecated Babel package (#65)

0.3.2
-----
- Fix for non-existent rst README

0.3.1
-----
- Update .gitignore
- Mark Yes and No for translation (#51) (#58)
- Mark 'No Items' for translation (#60)
- Set long_description in setup.py

0.3.0
-----
- Allow passing options to create_table (#41)
- Fix to use super in LinkCol.get_attr_list (#43)
- Refactor handling of HTML (#44)
- Add option to allow empty table (#45)
- Force env vars before imports in tests (#46)
- Add option to set attributes on element in ButtonCol (#47)
- Add option to pass url_kwargs_extra to LinkCol (#50)
- Add release.sh script
- Remove semi-duplicate README

0.2.13
------
- Add table border option (#40)

0.2.12
------
- Add NestedTableCol type
- Add test for NestedTableCol type
- Add entry to README.md for NestedTableCol type
- Add simple_nested.py example for NestedTableCol
- Add table_id keyword arg to Table initializer
- Add test for table_id field in Table initializer

0.2.11
------
- Fix tests for update to Babel
- Add config for read-the-docs
- Add better docs for the column types
- Fix some docs formatting
- Call to td_format for LinkCol td_contents.

0.2.10
------
- Fix DatetimeCol format option
- Formatting
- Fix to use super for Col subclasses

0.2.8
-----
- Add examples for setting classes attribute
- Add info to README about classes attribute
- Fix typos in README
- Add example for simple table within a flask app
- pep8 fix
- Reorder statements in tests/__init__ to keep pep8 happy
- Add option for setting a thead class
- Inherit columns when inheriting a parent table class

0.2.8
-----
- Add travis tests for python3.4
- Correct info about PYTHONPATH
- Use comprehensions rather than explicit for-loops
- Add option for setting 'No Items' text
- Add show option
- Add more tests for dynamic columns
- Add test for dynamic setting of no_items
- Add tests for sort_url being not-set
- Use coverage and coveralls in travis
- Install coverage for travis
- Don't use virtualenv path in travis
- Add coverage status to README
- Fix indenting in FuncItem in tests
- Give tests better names
- Use 'item' rather than 'i' for readability
- Make it easier to manipulate trs
- Add test and example for manipulating trs
- Add README info for overriding tr_format
- Change default value for attr_list
- Change dangerous default values
- Add docstrings for OptCol and BoolCol
- Add info on the included Col types
- Remove nested comprehension in tests
- Fix for if no value set for choices in OptCol
- Add test for when passing no value for choices to OptCol
- Add test for when passing no value for url_kwargs to LinkCol

0.2.7
-----
- Allow tables to be created dynamically
- Fix HTML in examples/simple.py
- Give dynamic example table a more classy name
- Add info to README about dynamically creating tables

0.2.6
-----
- Run pep8 with travis
- Tell travis to install pep8
- Add documentation about running examples
- Remove pointless shebang from sortable example
- Fix examples docs to not contain utter nonsense
- Make sortable example pass pep8
- Make tests pass pep8
- Run all python files through pep8 in Travis
- Make README and examples/simple.py use the same example
- Output example html in README
- Add newlines to output for readability
- Remove requirement for items to be len-able
- Add script for pep8 testing
- Fix README and simple example
- Tidy test_ten.html
- Add proper rst README file

0.2.5
-----
- Add build status to README (now that it's passing!)
- Make README clearer about loading from database
- Add subclassing example for RawCol
- Use unicode literals
- Prefer .format to %
- Use unicode literals in tests
- Prefer .format to % in tests
- Adjust spacing of imports
- PEP8 code

0.2.4
-----
- Declare encoding to fix unicode error
- Fix travis.yml

0.2.3
-----
- Add Sortable Tables to README
- Correct syntax error in __init__ method of table class

0.2.2
-----
- fix date_format parameter for DateCol
- fix unittests for people with different locale
- run tests via setup.py
- removed unnecessary str casting in order to support unicode
- fix for python3.3 problems
- Fix for travis to run tests with setup.py
- added method for formatting th-elements
- Update sortable example to include two-way sorting
- Integrate sortable tables

0.2.1
-----
- Use setuptools and fix dependencies

0.2.0
-----
- Remove cols() getter in table class
- Simplify use of attr and attr_list
- Add tests for more complex attr values used in url_kwargs in LinkCol
- Changed my mind about attr vs attr_list
- Add test for when attr_list items have dots in
- Add comment to attr_list example to justify having both attr and attr_list
- Add test for BoolCol
- Add tests for OptCol
- Add test for when there are no items
- Remove unused method
- Simplify imports for running tests
- Add test for setting table class when populating
- Add tests for DateCol and DatetimeCol
- Add test for getting content text for link from item via attr
- Improve HTML equivalence testing to help debugging tests
- Make tests not be locale dependent

0.1.7
-----
- Add LICENSE and README.md to MANIFEST.in

0.1.5
-----
- Initial release

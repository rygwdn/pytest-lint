pytest-lint
=============

py.test plugin for efficiently checking python source with pylint.


Usage
-----

install via::

    pip install git+https://github.com/rygwdn/pytest-lint.git

if you then type::

    py.test --lint

every file ending in ``.py`` will be discovered and run through pylint,
starting from the command line arguments.

 
Notes
-----

The repository of this plugin is at https://github.com/rygwdn/pytest-lint

For more info on py.test see http://pytest.org

The code is based on https://github.com/fschulze/pytest-flakes which is
partially based on Ronny Pfannschmidt's pytest-codecheckers plugin and Holger
Krekel's pytest-pep8.

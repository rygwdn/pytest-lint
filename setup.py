from setuptools import setup

setup(
    name='pytest-lint',
    description='pytest plugin to check source code with pylint',
    long_description=open("README.rst").read(),
    license="MIT license",
    version='0.2',
    author='Florian Schulze, Holger Krekel, Ronny Pfannschmidt, and Ryan Wooden',
    author_email='rygwdn@gmail.com',
    url='https://github.com/rygwdn/pytest-lint',
    py_modules=['pytest_lint'],
    entry_points={'pytest11': ['lint = pytest_lint']},
    install_requires=['pytest-cache', 'pytest>=2.7', 'pylint>=1.4'])

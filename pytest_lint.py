from pylint import lint
from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter

import _ast
import re
import py
import pytest
import sys


HISTKEY = "lint/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        '--lint', action='store_true',
        help="run pylint on .py files")


def pytest_sessionstart(session):
    config = session.config
    if config.option.lint:
        config._lintmtimes = config.cache.get(HISTKEY, {})


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.lint and path.ext == '.py':
        return LintItem(path, parent)


def pytest_sessionfinish(session):
    config = session.config
    if hasattr(config, "_lintmtimes"):
        config.cache.set(HISTKEY, config._lintmtimes)


class LintError(Exception):
    """ indicates an error during pylint checks. """


class LintItem(pytest.Item, pytest.File):

    def __init__(self, path, parent):
        super(LintItem, self).__init__(path, parent)
        if hasattr(self, 'add_marker'):
            self.add_marker("lint")
        else:
            self.keywords["lint"] = True

    def setup(self):
        lintmtimes = self.config._lintmtimes
        self._lintmtime = self.fspath.mtime()
        old = lintmtimes.get(str(self.fspath), 0)
        if old == self._lintmtime:
            pytest.skip("file(s) previously passed pylint checks")

    def runtest(self):
        # TODO: need to run these things in bulk!

        found_errors, out = check_file(self.fspath)
        if found_errors:
            raise LintError("\n".join(out))
        # update mtime only if test passed
        # otherwise failures would not be re-run next time
        self.config._lintmtimes[str(self.fspath)] = self._lintmtime

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(LintError):
            return excinfo.value.args[0]
        return super(LintItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "pylint-check")



class PytestReporter(BaseReporter):
    __implements__ = IReporter
    name = 'lint'
    extension = 'lint'

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, message):
        """Manage message of different type and in the context of path."""

        self.messages.append({
            'type': message.category,
            'module': message.module,
            'obj': message.obj,
            'line': message.line,
            'column': message.column,
            'path': message.path,
            'symbol': message.symbol,
            'message': escape(message.msg or ''),
        })

    def _display(self, layout):
        """Launch layouts display"""
        if self.messages:
            print(json.dumps(self.messages, indent=4), file=self.out)


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(JSONReporter)

def check_file(path):
    codeString = path.read()
    filename = py.builtin._totext(path)
    issues = []

    reporter = Reporter()
    lint.Run([], reporter=reporter, exit=False)

    for issues in reporter.issues:
        issues.append(
            '%s:%s: %s\n%s' % (
                warning.filename,
                warning.lineno,
                warning.__class__.__name__,
                warning.message % warning.message_args))

    return len(issues), issues

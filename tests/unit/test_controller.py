# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import random
import string
from unittest import mock

import pytest

import jrnl
from jrnl.args import parse_args
from jrnl.controller import _display_search_results


@pytest.fixture
def random_string():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=25))


@pytest.mark.parametrize("export_format", ["pretty", "short"])
@mock.patch("builtins.print")
@mock.patch("jrnl.controller.Journal.pprint")
def test_display_search_results_pretty_short(mock_pprint, mock_print, export_format):
    mock_args = parse_args(["--format", export_format])
    test_journal = mock.Mock(wraps=jrnl.journals.Journal)

    _display_search_results(mock_args, test_journal)

    mock_print.assert_called_once_with(mock_pprint.return_value)


@pytest.mark.parametrize(
    "export_format", ["markdown", "json", "xml", "yaml", "fancy", "dates"]
)
@mock.patch("jrnl.plugins.get_exporter")
@mock.patch("builtins.print")
def test_display_search_results_builtin_plugins(
    mock_print, mock_exporter, export_format, random_string
):
    test_filename = random_string
    mock_args = parse_args(["--format", export_format, "--file", test_filename])

    test_journal = mock.Mock(wraps=jrnl.journals.Journal)
    mock_export = mock.Mock()
    mock_exporter.return_value.export = mock_export

    _display_search_results(mock_args, test_journal)

    mock_exporter.assert_called_once_with(export_format)
    mock_export.assert_called_once_with(test_journal, test_filename)
    mock_print.assert_called_once_with(mock_export.return_value)

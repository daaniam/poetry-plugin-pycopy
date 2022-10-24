from pathlib import Path
import dataclasses

import pytest
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

from poetry_plugin_pycopy.pycopy import PoetryPluginPyCopyError, read_toml, read_config, parse_fields

from poetry_plugin_pycopy.models import PluginConfig


@pytest.mark.parametrize(
    'file_path, expected, is_error',
    [("valid_config_path", TOMLDocument, False), ("non_existing_path", PoetryPluginPyCopyError, True)],
)
def test_read_toml(file_path, expected, is_error, request):
    """Should read toml file"""

    file_path = request.getfixturevalue(file_path)

    if is_error:
        with pytest.raises(PoetryPluginPyCopyError, match=str(file_path)):
            read_toml(toml_path=file_path)
    else:

        result = read_toml(toml_path=file_path)
        assert isinstance(result, expected)


@pytest.mark.parametrize(
    'toml_data, expected, is_error',
    [
        ('valid_toml_data', PluginConfig, False),
        ('missing_config_in_toml', PoetryPluginPyCopyError, True),
        ('missing_config_key_in_toml', PoetryPluginPyCopyError, True),
    ],
)
def test_read_config(toml_data, expected, is_error, request):
    """Should read plugin config section from pyproject.toml"""

    toml_data = request.getfixturevalue(toml_data)

    if is_error:
        with pytest.raises(expected):
            read_config(toml_data=toml_data)
    else:
        plugin_config = read_config(toml_data=toml_data)
        assert dataclasses.is_dataclass(plugin_config)


def test_parse_fields(plugin_config, valid_toml_data):
    parsed = parse_fields(plugin_config, valid_toml_data)
    assert isinstance(parsed, dict)
    assert "name" and "version" and "description" in parsed.keys()
    assert "package_name" and "0.1.1" and "Some description" in parsed.values()


def test_pycopy():
    
from pathlib import Path

import pytest
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

from poetry_plugin_pycopy.pycopy import (
    PoetryPycopyPluginError,
    plugin_config,
    read_toml,
)

# @pytest.fixture
# def valid_config_path() -> Path:
#     return test_toml_samples.joinpath("valid-config.toml")


# @pytest.fixture
# def valid_toml_data(valid_config_path: Path) -> TOMLDocument:
#     return PyProjectTOML(path=valid_config_path).file.read()


def test_read_config_file(valid_toml_path: Path):
    """Should read toml file"""
    result = read_toml(toml_path=valid_toml_path)
    assert isinstance(result, TOMLDocument)
    assert "version" in result["tool"]["poetry"]


def test_config_file_not_found(invalid_toml_path: Path):
    """Should raise PoetryPycopyPluginError"""

    with pytest.raises(PoetryPycopyPluginError, match=str(invalid_toml_path)):
        read_toml(toml_path=invalid_toml_path)


def test_plugin_config(toml_data: TOMLDocument):
    """Should read plugin config section from toml file"""

    plugin_config(toml_data=toml_data)

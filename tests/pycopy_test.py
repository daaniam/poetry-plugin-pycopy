from pathlib import Path

import pytest
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

from poetry_plugin_pycopy.pycopy import (
    PoetryPycopyPluginError,
    read_config,
    read_toml,
)

# @pytest.fixture
# def valid_config_path() -> Path:
#     return test_toml_samples.joinpath("valid-config.toml")


# @pytest.fixture
# def valid_toml_data(valid_config_path: Path) -> TOMLDocument:
#     return PyProjectTOML(path=valid_config_path).file.read()


@pytest.mark.parametrize(
    'file_path, expected, is_error',
    [("valid_config_path", TOMLDocument, False), ("non_existing_path", PoetryPycopyPluginError, True)],
)
def test_read_config_file(file_path, expected, is_error, request):
    """Should read toml file"""

    file_path = request.getfixturevalue(file_path)

    if is_error:
        with pytest.raises(PoetryPycopyPluginError, match=str(file_path)):
            read_toml(toml_path=file_path)
    else:

        result = read_toml(toml_path=file_path)
        assert isinstance(result, expected)


def test_parse_fields()

# def test_config_file_not_found(non_existing_path: Path):
#     """Should raise PoetryPycopyPluginError"""

#     with pytest.raises(PoetryPycopyPluginError, match=str(non_existing_path)):
#         read_toml(toml_path=non_existing_path)


# def test_plugin_config(toml_data: TOMLDocument):
#     """Should read plugin config section from toml file"""

#     plugin_config(toml_data=toml_data)

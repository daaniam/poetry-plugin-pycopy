from pathlib import Path

import pytest
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument
from poetry_plugin_pycopy.models import PluginConfig

from poetry_plugin_pycopy.pycopy import read_toml, read_config

project_root: Path = Path(__name__).parent.absolute()
assets_dir: Path = project_root.joinpath("tests").joinpath("assets")
toml_samples: Path = assets_dir.joinpath("toml-samples")


@pytest.fixture
def valid_config_path() -> Path:
    return toml_samples.joinpath("valid-config.toml")


@pytest.fixture
def non_existing_path() -> Path:
    return toml_samples.joinpath("non-existing-file")


@pytest.fixture
def missing_config_path() -> Path:
    return toml_samples.joinpath("missing-config.toml")


@pytest.fixture
def missing_key_path() -> Path:
    return toml_samples.joinpath("missing-config-key.toml")


@pytest.fixture
def valid_toml_data(valid_config_path) -> TOMLDocument:
    return read_toml(toml_path=valid_config_path)


@pytest.fixture
def missing_config_in_toml(missing_config_path) -> TOMLDocument:
    return read_toml(toml_path=missing_config_path)


@pytest.fixture
def missing_config_key_in_toml(missing_key_path) -> TOMLDocument:
    return read_toml(toml_path=missing_key_path)


@pytest.fixture
def plugin_config(valid_toml_data) -> PluginConfig:
    return read_config(toml_data=valid_toml_data)

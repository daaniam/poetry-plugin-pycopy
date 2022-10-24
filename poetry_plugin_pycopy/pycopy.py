import json
from pathlib import Path

from models import PluginConfig
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

PLUGIN_NAME = "poetry-plugin-pycopy"
PROJECT_ROOT = Path(__name__).parent.absolute()
PROJECT_TOML_FILE = Path.joinpath(PROJECT_ROOT, "pyproject.toml")


class PoetryPluginPyCopyError(Exception):
    """PoetryPycopyPluginError"""


def create_line(k, v):
    """Create a line which will be written to a file.

    Example:
        __version = "1.0.4"
        __name = "My great app"

    """
    return f'__{k} = "{v}"\n'


def read_toml(toml_path: Path) -> TOMLDocument:
    """Read toml file

    Args:
        toml_path (Path): Path to .toml file

    Raises:
        PoetryPycopyPluginError: File not found

    Returns:
        TOMLDocument

    """

    # File not exists
    if not toml_path.exists():
        raise PoetryPluginPyCopyError(f"File not found {toml_path}")

    # Read file and return TOMLDocument object
    return PyProjectTOML(path=toml_path).data


def read_config(toml_data: TOMLDocument) -> PluginConfig:
    """Read [tool.poetry-pycopy-plugin] fields

    Args:
        toml_data: TOMLDocument

    Raises:
        PoetryPycopyPluginError: Field (key) not found in config section

    Returns:
        PluginConfig

    """

    # Verify that plugin config section exists in pyproject.toml
    try:
        toml_data["tool"][PLUGIN_NAME]
    except KeyError:
        raise PoetryPluginPyCopyError("Missing configuration in pyproject.toml")

    # Read config from pyproject.toml
    try:
        return PluginConfig(
            keys=list(toml_data["tool"][PLUGIN_NAME]["keys"]),
            dest_dir=toml_data["tool"][PLUGIN_NAME]["dest_dir"],
            dest_file=toml_data["tool"][PLUGIN_NAME]["dest_file"],
        )

    except KeyError as ex:
        raise PoetryPluginPyCopyError(ex)


def parse_fields(plugin_config: PluginConfig, toml_data: TOMLDocument) -> dict:
    """Parse requested keys from plugin config with keys from tool.poetry section.
    Only keys which exists in tool.poetry section will be returned.

    Args:
        plugin_config (PluginConfig): Plugin configuration
        toml_data (PyProjectTOML): Toml data

    Returns:
        dict: Parsed keys:values
    """

    # [tool.poetry] section
    tool_poetry = toml_data["tool"]["poetry"]

    # Find value in tool.poetry for every key from plugin configuration
    return {k: tool_poetry[k] for k in plugin_config.keys if k in tool_poetry}


def output_file_path(plugin_config: PluginConfig) -> Path:
    """Create path for output file from project root directory.

    Args:
        plugin_config (PluginConfig): Plugin configuration

    Returns:
        Path: Path to output file
    """
    return Path.joinpath(PROJECT_ROOT, plugin_config.dest_dir).joinpath(plugin_config.dest_file)


def pycopy():
    """Read pyproject.toml file from the project root, parse required fields and
    write them to the destination file.

    """

    print("\nRunning Poetry PyCopy Plugin:")

    toml_data: TOMLDocument = read_toml(toml_path=PROJECT_TOML_FILE)
    plugin_config: PluginConfig = read_config(toml_data=toml_data)

    # Destination file path
    dest_file_path = output_file_path(plugin_config)
    print("Destination file:", str(dest_file_path))

    # Parse
    parsed_data: dict = parse_fields(plugin_config, toml_data)
    print('\n', json.dumps(parsed_data, indent=2, default=str))

    # Create output-line for every record in parsed_data
    lines = [create_line(k, v) for k, v in parsed_data.items()]

    # Write lines to destination file
    with open(dest_file_path, "w+", encoding="utf-8") as f:
        f.writelines(lines)

    print("\n")

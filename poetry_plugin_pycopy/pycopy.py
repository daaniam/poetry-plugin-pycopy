import json
from pathlib import Path

from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

from .models import PluginConfig

PLUGIN_NAME = "poetry-pycopy-plugin"
PROJECT_ROOT = Path(__name__).parent.absolute()
PROJECT_TOML_FILE = Path.joinpath(PROJECT_ROOT, "pyproject.toml")


class PoetryPycopyPluginError(Exception):
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
        raise PoetryPycopyPluginError(f"File not found {toml_path}")

    # Read file and return TOMLDocument object
    return PyProjectTOML(path=toml_path).data


def plugin_config(toml_data: TOMLDocument) -> PluginConfig:
    """Read [tool.poetry-pycopy-plugin] fields

    Args:
        toml_data: TOMLDocument

    Raises:
        PoetryPycopyPluginError: Field (key) not found in config section

    Returns:
        PluginConfig

    """

    try:
        return PluginConfig(
            keys=list(toml_data["tool"][PLUGIN_NAME]["keys"]),
            dest_dir=toml_data["tool"][PLUGIN_NAME]["dest_dir"],
            dest_file=toml_data["tool"][PLUGIN_NAME]["dest_file"],
        )

    except KeyError as ex:
        raise PoetryPycopyPluginError(ex)


def parse_fields(plugin_config: PluginConfig, toml_data: PyProjectTOML) -> dict:
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


def pycopy():
    """Read pyproject.toml file from the project root, parse required fields and
    write them to the destination file.

    """

    print("\nRunning Poetry PyCopy Plugin:")

    toml_data: TOMLDocument = read_toml(toml_path=PROJECT_TOML_FILE)
    plugin_config: PluginConfig = plugin_config(toml_data=toml_data)

    # Destination file path
    pyproject_py = Path.joinpath(PROJECT_ROOT, plugin_config.dest_dir).joinpath(plugin_config.dest_file)
    print("Destination file:", str(pyproject_py))

    # Parse
    parsed_data = parse_fields(plugin_config, toml_data)
    print(json.dumps(parsed_data, indent=2, default=str))

    # Create output-line for every record in parsed_data
    lines = [create_line(k, v) for k, v in parsed_data.items()]

    # Write lines to destination file
    with open(pyproject_py, "w+", encoding="utf-8") as f:
        f.writelines(lines)

    print("\n")

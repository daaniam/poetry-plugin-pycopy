from cleo.events.console_events import TERMINATE
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin
from pathlib import Path
from poetry.core.pyproject.toml import PyProjectTOML
from poetry.console.commands.version import VersionCommand
from io import StringIO


def create_line(k, v):
    return f'__{k} = "{v}"\n'


class PushToPyprojectPy(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(TERMINATE, self.copy_pyproject_fields)

    def copy_pyproject_fields(
        self,
        event: ConsoleCommandEvent,
        event_name: str,
        dispatcher: EventDispatcher,
    ):

        # pyproject.toml file Path
        project_root = Path(__name__).parent.absolute()
        toml_file = Path.joinpath(project_root, "pyproject.toml")
        if not toml_file.exists():
            return

        # Read file
        toml_data = PyProjectTOML(path=toml_file).file.read()

        # [tool.poetry] fields
        tool_poetry = toml_data["tool"]["poetry"]

        # [tool.poetry-bump] fields - Plugin config
        try:
            copy_keys: list = list(toml_data["tool"]["poetry-bump"]["keys"])
            dest_dir: str = toml_data["tool"]["poetry-bump"]["dest_dir"]
            dest_file: str = toml_data["tool"]["poetry-bump"]["dest_file"]
        except KeyError:
            raise

        print("bump_keys", copy_keys)
        print("bump_dest_dir", dest_dir)
        print("bump_dest_file", dest_file)

        # Destination file path
        pyproject_py = Path.joinpath(project_root, dest_dir).joinpath(dest_file)

        # Find value in [tool.poetry] for every key in 'copy_keys'
        parsed_data = {k: tool_poetry[k] for k in copy_keys if k in tool_poetry}

        # Create line for every record in parsed_data
        lines = [create_line(k, v) for k, v in parsed_data.items()]

        # Write lines to destination file
        with open(pyproject_py, "w+", encoding="utf-8") as f:
            f.writelines(lines)

from traceback import print_tb
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
        application.event_dispatcher.add_listener(TERMINATE, self.push)

    def push(
        self,
        event: ConsoleCommandEvent,
        event_name: str,
        dispatcher: EventDispatcher,
    ):
        project_root = Path(__name__).parent.absolute()
        toml_file = Path.joinpath(project_root, "pyproject.toml")
        if not toml_file.exists():
            print("No toml file")

        toml_data = PyProjectTOML(path=toml_file).file.read()
        # poetry_tool = toml_data["tool"]["Poetry"]

        tool_poetry = toml_data["tool"]["poetry"]
        tool_poetry_name = toml_data["tool"]["poetry"]["name"]

        tool_poetry_bump = toml_data["tool"]["poetry-bump"]
        bump_keys = list(toml_data["tool"]["poetry-bump"]["keys"])
        bump_dest_dir = toml_data["tool"]["poetry-bump"]["dest_dir"]
        bump_dest_file = toml_data["tool"]["poetry-bump"]["dest_file"]

        print("bump_keys", bump_keys)
        print("bump_dest_dir", bump_dest_dir)
        print("bump_dest_file", bump_dest_file)

        pyproject_py = Path.joinpath(project_root, bump_dest_dir).joinpath(
            bump_dest_file
        )
        print("pyproject_py", pyproject_py)

        parsed_data = {k: tool_poetry[k] for k in bump_keys if k in tool_poetry}

        print("parsed_data", parsed_data)

        lines = [create_line(k, v) for k, v in parsed_data.items()]
        print("lines", lines)

        with open(pyproject_py, "w+", encoding="utf-8") as f:
            f.writelines(lines)

from cleo.commands.command import Command
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import TERMINATE
from cleo.events.event_dispatcher import EventDispatcher
from poetry.plugins.application_plugin import ApplicationPlugin
from .pycopy import pycopy


class PyCopyCommand(Command):

    name = "pycopy"
    description = "Copy fields from pyproject.toml to source"

    def handle(self) -> int:
        pycopy()
        return 0


def factory():
    return PyCopyCommand()


class PoetryPluginPycopy(ApplicationPlugin):
    """Plugin entrypoint class.

    Fire the plugin with the command "poetry pycopy" or "poetry version ..."
    The latter is there to auto-update data after version bump.
    """

    def activate(self, application):
        application.command_loader.register_factory("pycopy", factory)
        application.event_dispatcher.add_listener(TERMINATE, self.on_version_bump)

    def on_version_bump(
        self,
        event: ConsoleCommandEvent,
        event_name: str,
        dispatcher: EventDispatcher,
    ):

        if event.command.name == "version":
            pycopy()

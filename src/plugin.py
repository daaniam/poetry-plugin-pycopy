from cleo.events.console_events import TERMINATE
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PushToPyprojectPy(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(TERMINATE, self.push)

    def push(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ):
        print("Push META called")

    # def load_dotenv(
    #     self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    # ) -> None:
    #     command = event.command
    #     if not isinstance(command, EnvCommand):
    #         return

    #     io = event.io

    #     if io.is_debug():
    #         io.write_line("<debug>Loading environment variables.</debug>")

    #     load_dotenv()

import logging

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)


class StretchlyExtension(Extension):
    def __init__(self):
        super(StretchlyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        # Get the argument after the keyword (e.g., 'reset' or 'toggle')
        query = event.get_argument() or ""
        query = query.strip().lower()

        items = []

        # Define the available commands map
        # key: matching string
        # name: display title
        # script: the actual shell command to run
        commands = [
            {
                "key": "reset",
                "name": "Reset Stretchly",
                "description": "Resets breaks (flatpak run net.hovancik.Stretchly reset)",
                "script": "flatpak run net.hovancik.Stretchly reset",
            },
            {
                "key": "toggle",
                "name": "Toggle Stretchly",
                "description": "Pauses/Resumes breaks (flatpak run net.hovancik.Stretchly toggle)",
                "script": "flatpak run net.hovancik.Stretchly toggle",
            },
        ]

        # Filter items: show all if query is empty, otherwise match start of string
        for cmd in commands:
            if cmd["key"].startswith(query):
                items.append(
                    ExtensionResultItem(
                        icon="images/icon.svg",
                        name=cmd["name"],
                        description=cmd["description"],
                        on_enter=RunScriptAction(cmd["script"], []),
                    )
                )

        return RenderResultListAction(items)

import logging
from typing import List, Any, Dict

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

logger = logging.getLogger(__name__)

class Entry:
    __slots__: List[str] = [
        "__name",
        "__description",
        "__icon",
        "__aliases",
        "__command",
    ]

    def __init__(self, name: str, description: str, aliases: List[str], command: str, icon: str):
        self.__name = name
        self.__description = description
        self.__aliases = aliases
        self.__command = command
        self.__icon = icon

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def icon(self) -> str:
        return self.__icon

    @property
    def aliases(self) -> List[str]:
        return self.__aliases

    @property
    def command(self) -> str:
        return self.__command

class EntryIndex:
    __slots__: List[str] = ["__entries", "__aliases"]

    def __init__(self):
        # Instead of loading from JSON, we define our specific Stretchly commands here
        # to maintain the requested structure without external dependencies.
        raw_entries = [
            {
                "name": "Reset Stretchly",
                "description": "Resets breaks (flatpak run net.hovancik.Stretchly reset)",
                "aliases": ["reset", "r"],
                "command": "flatpak run net.hovancik.Stretchly reset",
                "icon": "images/icon.svg"
            },
            {
                "name": "Toggle Stretchly",
                "description": "Pauses/Resumes breaks (flatpak run net.hovancik.Stretchly toggle)",
                "aliases": ["toggle", "t", "pause", "resume"],
                "command": "flatpak run net.hovancik.Stretchly toggle",
                "icon": "images/icon.svg"
            }
        ]

        self.__entries: List[Entry] = [
            Entry(
                name=d["name"],
                description=d["description"],
                aliases=d["aliases"],
                command=d["command"],
                icon=d["icon"]
            ) for d in raw_entries
        ]
        self.__aliases: List[List[str]] = [entry.aliases for entry in self.__entries]

    @property
    def entries(self) -> List[Entry]:
        return self.__entries

    @property
    def aliases(self) -> List[List[str]]:
        return self.__aliases

class StretchlyExtension(Extension):
    def __init__(self):
        super(StretchlyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def __init__(self):
        self.__entries: EntryIndex = EntryIndex()
        self.__result_items: List[ExtensionResultItem] = [
            ExtensionResultItem(
                icon=entry.icon,
                name=entry.name,
                description=entry.description,
                on_enter=RunScriptAction(entry.command),
            )
            for entry in self.__entries.entries
        ]

    def on_event(self, event: KeywordQueryEvent, _) -> RenderResultListAction:
        arg: str = event.get_argument() or ""
        arg = arg.strip().lower()

        if arg:
            # Matches functionality of the requested structure using list comprehension
            return RenderResultListAction(
                [
                    self.__result_items[i]
                    for i, aliases in enumerate(self.__entries.aliases)
                    if any(arg in s for s in aliases)
                ]
            )
        else:
            return RenderResultListAction(self.__result_items)

if __name__ == '__main__':
    StretchlyExtension().run()

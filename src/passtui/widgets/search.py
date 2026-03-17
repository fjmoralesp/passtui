from textual import on
from textual.binding import Binding
from textual.widgets import Input
from passtui.widgets.pass_list import PassList
from typing import Any


class Search(Input):
    BINDINGS = [
        Binding("enter", "search", "Search"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, data: list[str], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.placeholder = "Type to search"
        self.data = data
        self.results = data

    def action_search(self) -> None:
        self.screen.focus_next(PassList)

    def action_cancel(self) -> None:
        self.clear()
        self.screen.focus_next()

    @on(Input.Changed)
    async def on_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.results = [
                entry for entry in self.data if event.value.lower() in entry.lower()
            ]
        else:
            self.results = self.data

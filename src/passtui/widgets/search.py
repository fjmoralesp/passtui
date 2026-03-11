from textual import on, work
from textual.widgets import Input
from typing import Any


class Search(Input):
    def __init__(self, data: list[str], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.placeholder = "Type to search"
        self.data = data
        self.results = data

    @on(Input.Changed)
    def on_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.results = [entry for entry in self.data if event.value in entry]
        else:
            self.results = self.data

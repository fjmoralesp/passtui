from textual.app import App
from textual import on
from textual.app import ComposeResult
from textual.widgets import Footer, Input, ListView
from passtui.security import passcli
from passtui.widgets.search import Search
from passtui.widgets.pass_list import PassList
from passtui.widgets.pass_data import PassData


class PassTUI(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Search(id="search", data=passcli.list_keys())
        yield PassList()
        yield PassData()
        yield Footer()

    @on(Input.Changed, "#search")
    def on_search_changed(self) -> None:
        pass_list = self.query_one(Search).results
        self.query_one(PassList).items = pass_list

    @on(ListView.Selected)
    def on_list_view_selected(self) -> None:
        selected_key = self.query_one(PassList).selected
        self.query_one(PassData).content = passcli.get_store_key(selected_key)

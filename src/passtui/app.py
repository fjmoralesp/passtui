from textual.app import App
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Input, Tree
from textual.widgets.tree import TreeNode
from passtui.security import passcli
from passtui.widgets.search import Search
from passtui.widgets.pass_list import PassList
from passtui.widgets.pass_data import PassData


class PassTUI(App):
    CSS_PATH = "app.tcss"
    keys = passcli.list_keys()

    BINDINGS = [
        Binding("/", "search_password", "Search password"),
        Binding("n", "add_new_password", "Add new password"),
        Binding("e", "focus_editor", "Focus editor"),
        Binding("t", "focus_explorer", "Focus explorer"),
        Binding("s", "sync", "Sync"),
        Binding("g", "create_gpg", "Create new GPG key"),
        Binding("x", "export_gpg", "Export GPG key"),
        Binding("z", "import_gpg", "Import GPG key"),
    ]

    """
    NOTES:
    - sync: should show a modal where the user adds a git repo url, and then we should sync the pass data to the repo
      if the pass store already has a repo we should sync with the repo every time the user adds a new pass or edits an existing one
      passpy should already do that, since pass itself does it.
    - create_gpg: should create a new gpg key and then add it to the store, the needed data should be request to the user in a modal
    - export_gpg: the implementation for this "gpg --export-secret-keys -a your_email@example.com > private.key" the needed data should be request to the user in a modal
    - import_gpg: the implementation for this "gpg --import private.key" the needed data should be request to the user in a modal
    """

    def compose(self) -> ComposeResult:
        yield Search(data=self.keys, id="search")
        yield PassList(items=self.keys)
        yield PassData()
        yield Footer()

    def action_search_password(self) -> None:
        self.screen.focus_next(Search)

    def action_focus_editor(self) -> None:
        self.query_one(PassData).text_area.focus()

    def action_focus_explorer(self) -> None:
        self.screen.focus_next(PassList)

    @on(Input.Changed, "#search")
    async def on_search_changed(self, event: Input.Changed) -> None:
        pass_list = self.query_one(Search).results
        widget: PassList = self.query_one(PassList)
        widget.is_filter = True if event.value else False
        widget.items = pass_list

    @on(Tree.NodeSelected)
    async def handle_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        self.update_selected(event.node)

    @work(exclusive=True)
    async def update_selected(self, node: TreeNode) -> None:
        if node.data:
            self.query_one(PassData).set_password(passcli.get_store_key(node.data))

    def action_add_new_password(self) -> None:
        self.query_one(PassData).add_new_password()

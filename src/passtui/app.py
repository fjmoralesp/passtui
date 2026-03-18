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
from passtui.screens.input_modal import InputModalScreen
from passtui.screens.gpg_keygen_modal import GpgKeygenModalScreen
from passtui.screens.gpg_export_modal import GpgExportModalScreen


class PassTUI(App):
    CSS_PATH = "app.tcss"
    keys = passcli.list_keys()

    BINDINGS = [
        Binding("/", "search_password", "Search password"),
        Binding("n", "add_new_password", "Add new password"),
        Binding("e", "focus_editor", "Focus editor"),
        Binding("t", "focus_explorer", "Focus explorer"),
        Binding("s", "sync", "Sync"),
        Binding("g", "create_gpg_store", "Create new GPG Store"),
        Binding("x", "export_gpg", "Export GPG key"),
        Binding("z", "import_gpg", "Import GPG key"),
    ]

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

    @work
    async def update_selected(self, node: TreeNode) -> None:
        if node.data:
            pass_model = passcli.get_store_key(node.data)
            if not pass_model:
                return
            self.query_one(PassData).set_password(
                pass_model=pass_model, pass_path=node.data
            )

    def action_add_new_password(self) -> None:
        self.query_one(PassData).add_new_password()

    @work
    async def action_sync(self) -> None:
        if passcli.is_git_initialized():
            passcli.sync_git()
            self.notify("Git sync completed")
        else:
            repo_url = await self.push_screen_wait(
                InputModalScreen(
                    "Enter git repository URL (e.g., git@github.com:user/repo.git)"
                )
            )
            if repo_url:
                try:
                    passcli.init_git(repo_url)
                    self.notify("Git initialized and pushed")
                except Exception as e:
                    self.notify(f"Failed to init git: {e}", severity="error")

    @work
    async def action_create_gpg_store(self) -> None:
        key_data = await self.push_screen_wait(GpgKeygenModalScreen())
        if key_data:
            try:
                fingerprint = passcli.create_gpg_store(
                    key_data.name, key_data.email, key_data.path
                )
                if not fingerprint:
                    self.notify("Failed to create GPG Store", severity="error")
                    return

                self.notify(f"GPG Store created: {fingerprint}")
            except Exception as e:
                self.notify(f"Error: {e}", severity="error")

    @work
    async def action_export_gpg(self) -> None:
        export_data = await self.push_screen_wait(GpgExportModalScreen())
        if export_data:
            try:
                output_path = passcli.export_gpg_key(
                    passphrase=export_data.passphrase,
                    output_path=export_data.output_path,
                )
                if not output_path:
                    self.notify("Failed to export GPG key", severity="error")
                    return

                self.notify(f"GPG key exported to {output_path}")
            except Exception as e:
                self.notify(f"Error: {e}", severity="error")

    @work
    async def action_import_gpg(self) -> None:
        filepath = await self.push_screen_wait(
            InputModalScreen(
                "Enter path to GPG key file (e.g., ~/passtui/gpg-export.asc)"
            )
        )
        if filepath:
            try:
                success = passcli.import_gpg_key(filepath)
                if not success:
                    self.notify("Failed to import GPG key", severity="error")
                    return

                self.notify("GPG key imported successfully")
            except Exception as e:
                self.notify(f"Error: {e}", severity="error")

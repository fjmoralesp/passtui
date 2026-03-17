from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from typing import Any


class PassList(Tree):
    items = reactive(list)
    is_filter = reactive(False)

    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down"),
        Binding("k", "cursor_up", "Cursor Up"),
        Binding("enter", "select_cursor", "Select"),
        Binding("c", "copy_password", "Copy password"),
        Binding("b", "copy_username", "Copy username"),
    ]

    def __init__(self, items: list[str], *args: Any, **kwargs: Any) -> None:
        super().__init__("List", *args, **kwargs)
        self.items = items
        self.show_root = False

    def watch_items(self) -> None:
        self._build_tree()
        if not self.is_filter:
            self.root.collapse_all()
            return

        self.root.expand_all()

    def on_mount(self) -> None:
        self._build_tree()
        self.focus()

    def _build_tree(self) -> None:
        self.root.remove_children()
        node_map: dict[tuple[str, ...], TreeNode] = {}

        for item in self.items:
            parts = item.split("/")
            start_index = self._find_existing_prefix_index(parts, node_map)
            parent = (
                self.root if start_index == 0 else node_map[tuple(parts[:start_index])]
            )
            self._create_nodes_from_parts(parts, start_index, parent, item, node_map)

    def _find_existing_prefix_index(
        self, parts: list[str], node_map: dict[tuple[str, ...], TreeNode]
    ) -> int:
        for i in range(len(parts), 0, -1):
            if tuple(parts[:i]) in node_map:
                return i
        return 0

    def _create_nodes_from_parts(
        self,
        parts: list[str],
        start_index: int,
        parent: TreeNode,
        data: str,
        node_map: dict[tuple[str, ...], TreeNode],
    ) -> None:
        for i in range(start_index, len(parts)):
            path = tuple(parts[: i + 1])
            node = (
                parent.add_leaf(parts[i], data=data)
                if i == len(parts) - 1
                else parent.add(parts[i], expand=False)
            )
            node_map[path] = node
            parent = node

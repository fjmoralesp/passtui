from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import TextArea, Static

DEFAULT_MESSAGE = "GPG locked. 🔐"
NEW_PASSWORD_TEMPLATE = """(add your password here)

Username:
URL:
Notes:
"""


class PassData(Static):
    text_area: TextArea

    _is_dirty = False
    _showing_welcome = True

    DEFAULT_CSS = """
    PassData {
        height: auto;
    }
    """

    # priority=True to override TextArea Bindings
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("i", "insert", "Insert"),
        Binding("c", "copy_password", "Copy password"),
        Binding("b", "copy_username", "Copy username"),
        Binding("y", "copy_current_line", "Copy current line"),
        Binding("j", "cursor_down", "Cursor Down"),
        Binding("k", "cursor_up", "Cursor Up"),
        Binding("ctrl+s", "save", "Save"),
    ]

    """
    NOTES:
    - copy_password (c): copy password to clipboard - uses pass's built-in clipboard (auto-clears after timeout)
    - copy_username (b): copy username to clipboard - parses pass text to get value after "Username:" label using pyperclip
    - copy_current_line (y): this should not be reusable, since its only meant to be user in this widget
      this should get the full text of the current TextArea line, then try to get the value by detecting the labels Username: URL: or Notes: and if not detected, just copy the whole line
    - j/k: cursor movement actions
    - ctrl+s behaves differently, depending whether it is editing an existing pass or adding a new one, if editing, it should save the changes, if adding, it should request the user in a modal, whether
      to add it in the selected pass in the PassList so the user should only provide the name of the new pass, or create a new entry in the store in which case the user should provide the full path of the pass
    """

    def compose(self) -> ComposeResult:
        self.text_area = TextArea.code_editor(
            DEFAULT_MESSAGE,
            language="markdown",
            read_only=True,
            show_line_numbers=False,
        )

        yield self.text_area

    def add_new_password(self) -> None:
        self._set_text(NEW_PASSWORD_TEMPLATE)
        self.action_insert()

    def set_password(self, pass_data: str) -> None:
        self._set_text(pass_data)
        self._set_read_only_mode()

    def action_cancel(self) -> None:
        self._set_read_only_mode()

    def action_insert(self) -> None:
        if self._showing_welcome:
            return

        self._is_dirty = True
        self._set_edit_mode()

    def _set_text(self, text: str) -> None:
        if not self._is_dirty:
            self.text_area.text = text
        self._showing_welcome = False

    def _set_edit_mode(self) -> None:
        self.text_area.read_only = False
        self.text_area.show_line_numbers = True
        self._focus_workaround_for_textual_bindings()

    def _set_read_only_mode(self) -> None:
        self.text_area.read_only = True
        self.text_area.show_line_numbers = True
        self._focus_workaround_for_textual_bindings()

    def _focus_workaround_for_textual_bindings(self) -> None:
        # Textual shows Bindings only when parent widget is focused first
        self.focus()
        self.text_area.focus()

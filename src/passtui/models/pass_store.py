from dataclasses import dataclass, fields


@dataclass(init=False)
class PassModel:
    """
    This model follows the passwordstore.org data organization.

    The copy features in `pass` and `passpy` copy only the first line of an
    entry. Following the recommended pattern:

        "This is the preferred organizational scheme used by the author. The
        --clip / -c options will only copy the first line of such a file to the
        clipboard, thereby making it easy to fetch the password for login forms,
        while retaining additional information in the same file."

    Reference: https://www.passwordstore.org/
    """

    password: str
    username: str
    url: str
    meta: list[str]

    _raw_data: str
    _template_ignored: tuple[str, ...] = (
        "_template_ignored",
        "password",
        "_raw_data",
        "meta",
    )

    def __init__(self, data: str | None) -> None:
        if data is None:
            lines = []
        else:
            lines = data.strip().split("\n")

        password = lines[0] if lines else ""
        username = ""
        url = ""
        meta = []

        for line in lines[1:]:
            if line.startswith("Username:"):
                username = line.split(":", 1)[1].strip()
            elif line.startswith("URL:"):
                url = line.split(":", 1)[1].strip()
            else:
                meta.append(line.strip())

        self.password = password
        self.username = username
        self.url = url
        self.meta = meta
        self._raw_data = data if data is not None else ""

    def __str__(self) -> str:
        return self._raw_data

    @classmethod
    def get_new_entry_template(cls) -> tuple[PassModel, str]:
        lines = ["(add your password here)"]
        for field in fields(cls):
            if field.name not in cls._template_ignored:
                lines.append(f"{field.name.capitalize()}: ")
        template = "\n".join(lines)
        return cls(template), template

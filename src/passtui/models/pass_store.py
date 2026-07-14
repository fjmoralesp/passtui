from dataclasses import dataclass, field, fields


@dataclass(init=False)
class PassModel:
    password: str
    username: str = field(metadata={"in_template": True})
    url: str = field(metadata={"in_template": True})
    meta: list[str]

    _raw_data: str

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
    def get_new_entry_template(cls) -> tuple["PassModel", str]:
        lines = ["(add your password here)"]
        for declared_field in fields(cls):
            if declared_field.metadata.get("in_template"):
                lines.append(f"{declared_field.name.capitalize()}: ")
        template = "\n".join(lines)
        return cls(template), template

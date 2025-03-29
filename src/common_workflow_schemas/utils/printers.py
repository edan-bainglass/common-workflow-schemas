import json
import typing as t


def print_json(
    obj: t.Any,
    indent: int = 2,
    sort_keys: bool = False,
    separators: t.Tuple[str, str] = (", ", ": "),
) -> None:
    """Pretty print a JSON object."""
    print(
        json.dumps(
            obj,
            indent=indent,
            sort_keys=sort_keys,
            separators=separators,
        )
    )

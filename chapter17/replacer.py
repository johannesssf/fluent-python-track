# Returns an iterator of tuples of strings
from collections.abc import Iterable

FromTo = tuple[str, str]  # 1


def zip_replace(text: str, changes: Iterable[FromTo]) -> str:  # 2
    for from_, to in changes:
        text = text.replace(from_, to)
    return text

from __future__ import annotations
from typing import get_type_hints


def clip(text: str, max_len: int = 80) -> str:
    ...


if __name__ == '__main__':
    print(clip.__annotations__)
    print(get_type_hints(clip))

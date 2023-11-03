from typing import TypedDict


class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int


if __name__ == '__main__':
    pp = BookDict(
        title='Programming Pearls',  # 1
        authors='Jon Bentley',   # 2
        isbn='0201657880',
        pagecount=256,
    )
    print(pp)  # 3
    print(type(pp))
    # pp.title  # 4
    print(pp['title'])
    print(BookDict.__annotations__)  # 5

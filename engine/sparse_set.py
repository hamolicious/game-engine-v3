from typing import Generic, TypeVar

T = TypeVar("T")


class SparseSet(Generic[T]):
    def __init__(self) -> None:
        self.sparse: dict[T, int] = {}
        self.dense: list[T] = []

    def insert(self, value: T) -> int:
        self.sparse[value] = len(self.dense)
        self.dense.append(value)

        return self.sparse[value]

    def remove(self, value: T) -> bool:
        if value not in self.sparse:
            return False
        index = self.sparse[value]
        last = self.dense[-1]
        self.dense[index] = last
        self.sparse[last] = index
        self.dense.pop()
        del self.sparse[value]
        return True

    def contains(self, value: T) -> bool:
        return value in self.sparse

    def __len__(self) -> int:
        return len(self.dense)

    def __iter__(self):
        yield from self.dense


if __name__ == "__main__":
    sset = SparseSet[int]()
    sset.insert(3)
    sset.insert(5)
    print(3 in sset)  # True
    print(2 in sset)  # False
    sset.remove(3)
    print(3 in sset)  # False
    for value in sset:
        print(value)

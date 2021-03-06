"""Abstract Base Class for a NVD feed adapter -- converts storage operations to target interface."""
import random
import typing

from abc import ABC, abstractmethod

from nvdlib.model import Document


class BaseCursor(ABC):
    """Abstract base class for adapter cursor."""

    @abstractmethod
    def next(self) -> Document:
        """Return next element."""

    @abstractmethod
    def next_batch(self, batch_size: int = None) -> typing.List[Document]:
        """Return next batch of elements."""

    @abstractmethod
    def batch_size(self, batch_size: int):
        """Set batch size."""


class BaseAdapter(ABC):
    """Abstract class defining storage adapter."""

    def __init__(self, name: str):
        self._name: str = name
        self._storage: typing.Any = None

        self._data: typing.Any = None

        self._cursor: typing.Any = None

    def __iter__(self):
        self._cursor = self.cursor()
        self._cursor.batch_size(1)

        return self

    def __next__(self):
        if not self._cursor:
            raise Exception("Iterator has not been initialized. Cannot call `__next__` method.")

        return self._cursor.next()

    @property
    def storage(self) -> typing.Any:
        return self._storage

    @property
    def name(self):
        return self._name

    @abstractmethod
    def connect(self, storage: str = None):
        """Connect adapter adapter to a storage."""

    @abstractmethod
    def process(self, data: typing.Iterable["Document"]):
        """Process given data and store in connected storage."""

    @abstractmethod
    def find(self, selectors: typing.Dict[str, typing.Any] = None, limit: int = None):
        """Find documents based on given selectors."""

    @abstractmethod
    def dump(self, storage: typing.Any = None):
        """Dump stored data into a storage."""

    @abstractmethod
    def count(self) -> int:
        """Return number of documents in the collection."""

    @abstractmethod
    def cursor(self) -> BaseCursor:
        """Initialize cursor to the beginning of a collection.

        The cursor must have implemented at least the following functionality:
            - next() ->
            - batch_size()
        """

    def sample(self, sample_size: int = 20):
        """Draw random sample."""
        return random.choices(
            [item for item in self._data if item is not None],
            k=sample_size
        )


from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Self


class Producer[T](AbstractContextManager["Producer[T]", None], Iterator[T], ABC):
    """A synchronous producer of ``T`` values.

    Values can be consumed either by explicit calls to :meth:`read` or
    by iterating with ``for``. The producer is also a context manager:
    entering the ``with`` block calls :meth:`open`, and exiting it
    calls :meth:`close`, even when an exception propagates out of the
    block.

    Subclasses must implement :meth:`open`, :meth:`read`, and
    :meth:`close`. The iterator protocol is provided by delegating
    ``__next__`` to :meth:`read`; signal exhaustion by raising
    :exc:`StopIteration` from :meth:`read`.
    """

    # Content manager

    def __enter__(self) -> Self:
        self.open()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    # Iterator

    def __next__(self) -> T:
        return self.read()

    # Abstract methods

    @abstractmethod
    def open(self) -> None:
        """Acquire any resources required to produce values.

        Called automatically on ``__enter__`` before any call to
        :meth:`read`. Implementations should be idempotent: opening an
        already-open producer must not raise.
        """

    @abstractmethod
    def close(self) -> None:
        """Release any resources held by the producer.

        Called automatically on ``__exit__``. Implementations should be
        idempotent: closing an already-closed producer must not raise.
        """

    @abstractmethod
    def read(self) -> T:
        """Return the next value from the producer.

        Raises:
            StopIteration: When the producer has been exhausted and no
                further values are available.
        """


class Consumer[T](AbstractContextManager["Consumer[T]", None], ABC):
    """A synchronous consumer of ``T`` values.

    Values are submitted by calling :meth:`write`. The consumer is also
    a context manager: entering the ``with`` block calls :meth:`open`,
    and exiting it calls :meth:`close`, even when an exception
    propagates out of the block.

    Subclasses must implement :meth:`open`, :meth:`write`, and
    :meth:`close`.
    """

    # Content manager

    def __enter__(self) -> Self:
        self.open()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    # Abstract methods

    @abstractmethod
    def open(self) -> None:
        """Acquire any resources required to accept values.

        Called automatically on ``__enter__`` before any call to
        :meth:`write`. Implementations should be idempotent: opening an
        already-open consumer must not raise.
        """

    @abstractmethod
    def close(self) -> None:
        """Release any resources held by the consumer.

        Called automatically on ``__exit__``. Implementations should be
        idempotent: closing an already-closed consumer must not raise.
        """

    @abstractmethod
    def write(self, value: T) -> None:
        """Submit the next value to the consumer."""


class Stream[T, S](Producer[T], Consumer[S], ABC):
    """A bidirectional synchronous stream that both produces and consumes values.

    Produces values of type ``T`` via :meth:`read` and accepts values
    of type ``S`` via :meth:`write`.
    """

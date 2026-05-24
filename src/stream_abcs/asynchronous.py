from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Self


class AsyncProducer[T](
    AbstractAsyncContextManager["AsyncProducer[T]", None],
    AsyncIterator[T],
    ABC,
):
    """An asynchronous producer of ``T`` values.

    Values can be consumed either by explicit calls to :meth:`read` or
    by iterating with ``async for``. The producer is also an async
    context manager: entering the ``async with`` block calls
    :meth:`open`, and exiting it calls :meth:`close`, even when an
    exception propagates out of the block.

    Subclasses must implement :meth:`open`, :meth:`read`, and
    :meth:`close`. The iterator protocol is provided by delegating
    ``__anext__`` to :meth:`read`; signal exhaustion by raising
    :exc:`StopAsyncIteration` from :meth:`read`.
    """

    # Content manager

    async def __aenter__(self) -> Self:
        await self.open()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    # Iterator

    async def __anext__(self) -> T:
        return await self.read()

    # Abstract methods

    @abstractmethod
    async def open(self) -> None:
        """Acquire any resources required to produce values.

        Called automatically on ``__aenter__`` before any call to
        :meth:`read`. Implementations should be idempotent: opening an
        already-open producer must not raise.
        """

    @abstractmethod
    async def close(self) -> None:
        """Release any resources held by the producer.

        Called automatically on ``__aexit__``. Implementations should be
        idempotent: closing an already-closed producer must not raise.
        """

    @abstractmethod
    async def read(self) -> T:
        """Return the next value from the producer.

        Raises:
            StopAsyncIteration: When the producer has been exhausted and
                no further values are available.
        """


class AsyncConsumer[T](AbstractAsyncContextManager["AsyncConsumer[T]", None], ABC):
    """An asynchronous consumer of ``T`` values.

    Values are submitted by calling :meth:`write`. The consumer is also
    an async context manager: entering the ``async with`` block calls
    :meth:`open`, and exiting it calls :meth:`close`, even when an
    exception propagates out of the block.

    Subclasses must implement :meth:`open`, :meth:`write`, and
    :meth:`close`.
    """

    # Content manager

    async def __aenter__(self) -> Self:
        await self.open()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    # Abstract methods

    @abstractmethod
    async def open(self) -> None:
        """Acquire any resources required to accept values.

        Called automatically on ``__aenter__`` before any call to
        :meth:`write`. Implementations should be idempotent: opening an
        already-open consumer must not raise.
        """

    @abstractmethod
    async def close(self) -> None:
        """Release any resources held by the consumer.

        Called automatically on ``__aexit__``. Implementations should be
        idempotent: closing an already-closed consumer must not raise.
        """

    @abstractmethod
    async def write(self, value: T) -> None:
        """Submit the next value to the consumer."""


class AsyncStream[T, S](AsyncProducer[T], AsyncConsumer[S], ABC):
    """A bidirectional asynchronous stream that both produces and consumes values.

    Produces values of type ``T`` via :meth:`read` and accepts values
    of type ``S`` via :meth:`write`.
    """

from abc import ABC
from collections.abc import Sequence

from stream_abcs.asynchronous import AsyncConsumer, AsyncProducer
from stream_abcs.synchronous import Consumer, Producer


class Batch[T](Sequence[T], ABC):
    """A finite ordered group of ``T`` values handled as a single unit.

    Subclasses inherit the :class:`~collections.abc.Sequence` interface
    and need only implement ``__getitem__`` and ``__len__``; the
    remaining sequence methods are derived from those.
    """


class Batcher[T](Consumer[T], Producer[Batch[T]], ABC):
    """A consumer of ``T`` values that produces :class:`Batch` instances.

    Values written to the batcher are accumulated and later emitted as
    :class:`Batch` instances when read. Implementations choose the
    policy that determines when a batch is ready, such as a maximum
    size or a maximum delay.
    """


class AsyncBatcher[T](AsyncConsumer[T], AsyncProducer[Batch[T]], ABC):
    """An async consumer of ``T`` values that produces :class:`Batch` instances.

    Values written to the batcher are accumulated and later emitted as
    :class:`Batch` instances when read. Implementations choose the
    policy that determines when a batch is ready, such as a maximum
    size or a maximum delay.
    """

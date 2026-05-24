from abc import ABC, abstractmethod

from stream_abcs.asynchronous import AsyncStream
from stream_abcs.synchronous import Stream


class Acknowledgement[T](ABC):  # noqa: B024
    """A signal confirming that a value of type ``T`` has been processed.

    Acknowledgements flow in the reverse direction of the values they refer
    to: a component that emits values of type ``T`` expects to later receive
    ``Acknowledgement[T]`` instances confirming their handling, and a
    component that consumes values of type ``T`` is responsible for
    producing the corresponding acknowledgements once processing is
    complete.
    """


class AcknowledgedProducer[T](Stream[T, Acknowledgement[T]], ABC):
    """A producer of ``T`` values that consumes acknowledgements for them."""


class AcknowledgedConsumer[T](Stream[Acknowledgement[T], T], ABC):
    """A consumer of ``T`` values that produces acknowledgements for them."""


class AcknowledgedStream[T, S](ABC):
    """A bidirectional stream with acknowledgements flowing in both directions.

    Produces values of type ``T`` and expects to consume ``Acknowledgement[T]``
    instances, while simultaneously consuming values of type ``S`` from and
    producing ``Acknowledgement[S]`` instances.
    """

    @property
    @abstractmethod
    def producer(self) -> AcknowledgedProducer[T]: ...

    @property
    @abstractmethod
    def consumer(self) -> AcknowledgedConsumer[S]: ...


class AcknowledgedAsyncProducer[T](AsyncStream[T, Acknowledgement[T]], ABC):
    """An async producer of ``T`` values that consumes acknowledgements for them."""


class AcknowledgedAsyncConsumer[T](AsyncStream[Acknowledgement[T], T], ABC):
    """An async consumer of ``T`` values that produces acknowledgements for them."""


class AcknowledgedAsyncStream[T, S](ABC):
    """A bidirectional async stream with acknowledgements flowing in both directions.

    Produces values of type ``T`` and expects to consume ``Acknowledgement[T]``
    instances, while simultaneously consuming values of type ``S`` from and
    producing ``Acknowledgement[S]`` instances.
    """

    @property
    @abstractmethod
    def producer(self) -> AcknowledgedAsyncProducer[T]: ...

    @property
    @abstractmethod
    def consumer(self) -> AcknowledgedAsyncConsumer[S]: ...

# stream-abcs

Abstract base classes for producers, consumers, and bidirectional streams in Python.

`stream-abcs` defines a small, opinionated set of interfaces for components that produce values, consume values, or do both. Each interface is a context manager that manages its own resources, and the producer interfaces also implement the iterator protocol. Synchronous, asynchronous, and acknowledgement-aware variants are provided.

The package has no runtime dependencies and requires Python 3.12+ (it uses [PEP 695](https://peps.python.org/pep-0695/) type parameter syntax).

## Installation

```bash
pip install stream-abcs
```

## The interfaces

### Synchronous

| Class | Role |
| --- | --- |
| `Producer[T]` | Produces values of type `T`. Iterable; raise `StopIteration` from `read()` to signal exhaustion. |
| `Consumer[T]` | Accepts values of type `T` via `write()`. |
| `Stream[T, S]` | Produces `T` and consumes `S`. |

Subclasses implement `open()`, `close()`, and `read()` / `write()`. Entering the `with` block calls `open()`; leaving it calls `close()`, even on exception. Implementations of `open()` and `close()` should be idempotent.

### Asynchronous

`AsyncProducer[T]`, `AsyncConsumer[T]`, and `AsyncStream[T, S]` mirror their synchronous counterparts. They are async context managers, `AsyncProducer` is an async iterator, and the abstract methods are coroutines. Signal exhaustion with `StopAsyncIteration`.

### Acknowledged

The acknowledged variants pair every produced value with an acknowledgement flowing back in the opposite direction.

- `Acknowledgement[T]` — a signal that a value of type `T` has been processed.
- `AcknowledgedProducer[T]` — produces `T`, consumes `Acknowledgement[T]`.
- `AcknowledgedConsumer[T]` — consumes `T`, produces `Acknowledgement[T]`.
- `AcknowledgedStream[T, S]` — exposes a `producer` of `T` and a `consumer` of `S`, each with their own acknowledgement channel.

`AcknowledgedAsyncProducer`, `AcknowledgedAsyncConsumer`, and `AcknowledgedAsyncStream` are the async equivalents.

## Examples

### Implementing a synchronous producer

```python
from stream_abcs import Producer


class RangeProducer(Producer[int]):
    def __init__(self, stop: int) -> None:
        self._stop = stop
        self._i = 0

    def open(self) -> None:
        self._i = 0

    def close(self) -> None:
        pass

    def read(self) -> int:
        if self._i >= self._stop:
            raise StopIteration
        value = self._i
        self._i += 1
        return value


with RangeProducer(3) as producer:
    for value in producer:
        print(value)
```

### Implementing an asynchronous consumer

```python
from stream_abcs import AsyncConsumer


class PrintConsumer(AsyncConsumer[str]):
    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def write(self, value: str) -> None:
        print(value)


async def main() -> None:
    async with PrintConsumer() as consumer:
        await consumer.write("hello")
```

## Development

The project uses [uv](https://docs.astral.sh/uv/) for environment management, [ruff](https://docs.astral.sh/ruff/) for linting, and [mypy](https://mypy.readthedocs.io/) in strict mode for type checking.

```bash
uv sync
uv run ruff check
uv run mypy src
```
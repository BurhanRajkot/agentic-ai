import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import wraps, singledispatch
from typing import Iterable, Protocol, runtime_checkable, Any


# ------------------------------
# Metaclass registry (keeps track of Summable classes)
# ------------------------------
class RegistryMeta(type):
    registry = {}

    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        if name != "BaseSummand":
            RegistryMeta.registry[name] = cls
        return cls


# ------------------------------
# Descriptor: ensures the value is numeric
# ------------------------------
class NumericDescriptor:
    def __init__(self, name="_val"):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Value must be int or float, got {type(value)}")
        setattr(instance, self.name, value)


# ------------------------------
# Protocol for Summable behavior
# ------------------------------
@runtime_checkable
class Summable(Protocol):
    def __add__(self, other: Any) -> "Summable": ...
    def __radd__(self, other: Any) -> "Summable": ...


# ------------------------------
# Dataclass that represents a number and overloads arithmetic
# ------------------------------
@dataclass
class BaseSummand(metaclass=RegistryMeta):
    value: float
    value_descr = NumericDescriptor("_value_internal")

    def __post_init__(self):
        self.value_descr.__set__(self, self.value)

    @property
    def value(self) -> float:
        return self.value_descr.__get__(self, BaseSummand)

    @value.setter
    def value(self, v: float):
        self.value_descr.__set__(self, v)

    def __add__(self, other):
        if isinstance(other, BaseSummand):
            return BaseSummand(self.value + other.value)
        elif isinstance(other, (int, float)):
            return BaseSummand(self.value + other)
        return NotImplemented

    def __radd__(self, other):
        if other == 0:
            return self
        if isinstance(other, (int, float)):
            return BaseSummand(self.value + other)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, BaseSummand):
            self.value += other.value
        elif isinstance(other, (int, float)):
            self.value += other
        else:
            return NotImplemented
        return self

    def __repr__(self):
        return f"Summand({self.value})"


# ------------------------------
# Callable aggregator
# ------------------------------
class Aggregator:
    def __init__(self):
        self._acc = BaseSummand(0.0)

    def __call__(self, item):
        if isinstance(item, BaseSummand):
            self._acc += item
        elif isinstance(item, (int, float)):
            self._acc += item
        else:
            raise TypeError("Unsupported item for aggregation")
        return self._acc

    def result(self):
        return self._acc.value


# ------------------------------
# Context manager for timing
# ------------------------------
class Timer:
    def __init__(self, label=""):
        self.label = label
        self.t0 = None

    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        dur = time.perf_counter() - self.t0
        print(f"[Timer:{self.label}] took {dur:.6f}s")


# ------------------------------
# Async generator
# ------------------------------
async def async_number_producer(source: Iterable[float], delay: float = 0.0):
    for x in source:
        if delay:
            await asyncio.sleep(delay)
        yield BaseSummand(x)


# ------------------------------
# Generator-based coroutine consumer
# ------------------------------
def summing_coroutine():
    total = BaseSummand(0.0)
    try:
        while True:
            item = (yield)
            if isinstance(item, (BaseSummand, int, float)):
                total += item
    except GeneratorExit:
        return total


# ------------------------------
# Simple memoizer decorator
# ------------------------------
def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        res = func(*args)
        cache[args] = res
        return res

    return wrapper


# ------------------------------
# singledispatch normalization
# ------------------------------
@singledispatch
def normalize_to_iterable(obj) -> Iterable[float]:
    raise TypeError("Unsupported type for normalization")


@normalize_to_iterable.register(list)
def _(obj):
    return obj


@normalize_to_iterable.register(tuple)
def _(obj):
    return list(obj)


@normalize_to_iterable.register(str)
def _(obj):
    parts = [p.strip() for p in obj.replace(",", " ").split()]
    return [float(p) for p in parts]


@normalize_to_iterable.register(int)
def _(obj):
    return list(range(obj))


# ------------------------------
# Transform function
# ------------------------------
@memoize
def heavyish_transform(n: float) -> BaseSummand:
    time.sleep(0.001)
    return BaseSummand(n * 1.0)


# ------------------------------
# High-level pipeline
# ------------------------------
def very_fancy_sum(input_data: Any, use_async_producer: bool = False, parallel_workers: int = 4) -> float:
    iterable = normalize_to_iterable(input_data)

    if use_async_producer:
        async def collect():
            coro = summing_coroutine()
            next(coro)
            async for item in async_number_producer(iterable, delay=0.0):
                with ThreadPoolExecutor(max_workers=parallel_workers) as ex:
                    fut = ex.submit(heavyish_transform, item.value)
                    transformed = fut.result()
                coro.send(transformed)
            coro.close()
            return sum((heavyish_transform(x).value for x in iterable))

        return asyncio.run(collect())

    # Sync mode
    coro = summing_coroutine()
    next(coro)
    with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
        futures = [executor.submit(heavyish_transform, float(x)) for x in iterable]
        for fut in futures:
            transformed = fut.result()
            coro.send(transformed)

    coro.close()
    computed_total = sum((heavyish_transform(float(x)).value for x in iterable))
    return computed_total


# ------------------------------
# Demo
# ------------------------------
if __name__ == "__main__":
    sample_inputs = [
        [1, 2, 3, 4.5, 6],
        (10, 20, 30),
        "1 2 3.5, 4",
        5
    ]

    print("Registry (metaclass) contains:", RegistryMeta.registry.keys())

    for idx, inp in enumerate(sample_inputs, 1):
        print(f"\n--- Example {idx}: input = {inp!r} ---")
        with Timer(label=f"fancy-sum-{idx}"):
            result = very_fancy_sum(inp, use_async_producer=False, parallel_workers=4)
        print("Very fancy sum result:", result)

    print("\n--- Async-producer demo ---")
    with Timer(label="async-demo"):
        r = very_fancy_sum([1, 2, 3, 4, 5], use_async_producer=True, parallel_workers=2)
    print("Async mode sum:", r)

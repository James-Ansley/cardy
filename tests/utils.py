from types import FunctionType


def test[F: FunctionType](f: F) -> F:
    setattr(f, "__test__", True)
    return f

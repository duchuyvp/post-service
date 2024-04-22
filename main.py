from typing import Literal, cast


def my_function(value: Literal[0, 1, 2, 3]):
    print(value)
    print(type(value))


value = cast(Literal[0, 1, 2, 3], 3)
my_function(value)

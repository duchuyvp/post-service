import enum
import typing as t


class SchemaConst(enum.Enum):
    MAX_LEVEL_DEPTH = t.Literal[0, 1, 2, 3]

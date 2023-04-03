from collections import defaultdict
from dataclasses import fields, is_dataclass
from typing import Any


def reset_all_to_defaults(dataclass_inst: Any) -> None:
    """
    Reset all dataclass variables to defaults.
    if a field of the class is dataclass object, recursion call is made.
    Otherwise reset each field to default.
    Field types that acceptable: Dataclass, DefaultDict, primitives.
    :param dataclass_inst: dataclass object
    :type dataclass_inst: Any
    """

    # iterate over fields
    for class_field in fields(dataclass_inst):

        # get field value
        field_value = getattr(dataclass_inst, class_field.name)

        # if the value is a nested dataclass, make a recursion call
        if is_dataclass(field_value):
            reset_all_to_defaults(field_value)

        # if the value is complex(dict) reset it
        elif isinstance(field_value, defaultdict):
            setattr(dataclass_inst, class_field.name, defaultdict(int))

        # if value is a primitive reset it
        else:
            setattr(dataclass_inst, class_field.name, class_field.default)

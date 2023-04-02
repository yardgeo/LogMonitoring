from collections import defaultdict
from dataclasses import fields, is_dataclass


def dataclass_equal_to_defaults(dataclass_inst) -> bool:
    for class_field in fields(dataclass_inst):
        field_value = getattr(dataclass_inst, class_field.name)
        if is_dataclass(field_value):
            if not dataclass_equal_to_defaults(field_value):
                return False
        elif isinstance(field_value, defaultdict):
            if field_value:
                return False
        else:
            if field_value != class_field.default:
                return False
    return True

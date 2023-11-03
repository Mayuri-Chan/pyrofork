from dataclasses import dataclass
from typing import Optional, Union, List


@dataclass
class Identifier:
    inline_message_id: Optional[Union[str, List[str]]] = None
    chat_id: Optional[Union[Union[int, str], List[Union[int, str]]]] = None
    message_id: Optional[Union[int, List[int]]] = None
    from_user_id: Optional[Union[Union[int, str], List[Union[int, str]]]] = None

    def matches(self, update: "Identifier") -> bool:
        # Compare each property of other with the corresponding property in self
        # If the property in self is None, the property in other can be anything
        # If the property in self is not None, the property in other must be the same
        for field in self.__annotations__:
            pattern_value = getattr(self, field)
            update_value = getattr(update, field)

            if pattern_value is not None:
                if isinstance(update_value, list):
                    if isinstance(pattern_value, list):
                        if not set(update_value).intersection(set(pattern_value)):
                            return False
                    elif pattern_value not in update_value:
                        return False
                elif isinstance(pattern_value, list):
                    if update_value not in pattern_value:
                        return False
                elif update_value != pattern_value:
                    return False
        return True

    def count_populated(self):
        non_null_count = 0

        for attr in self.__annotations__:
            if getattr(self, attr) is not None:
                non_null_count += 1

        return non_null_count
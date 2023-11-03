from dataclasses import dataclass
from typing import Optional


@dataclass
class Identifier:
    inline_message_id: Optional[str] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    from_user_id: Optional[int] = None

    def matches(self, other: "Identifier") -> bool:
        # Compare each property of other with the corresponding property in self
        # If the property in self is None, the property in other can be anything
        # If the property in self is not None, the property in other must be the same
        for field in self.__annotations__:
            self_value = getattr(self, field)
            other_value = getattr(other, field)

            if self_value is not None and other_value != self_value:
                return False
        return True

    def count_populated(self):
        non_null_count = 0

        for attr in self.__annotations__:
            if getattr(self, attr) is not None:
                non_null_count += 1

        return non_null_count
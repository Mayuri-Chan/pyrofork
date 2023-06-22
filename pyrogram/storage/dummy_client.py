from pymongo.client_session import TransactionOptions
from bson.codec_options import CodecOptions
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import (
    Nearest,
    Primary,
    PrimaryPreferred,
    Secondary,
    SecondaryPreferred,
)
from pymongo.write_concern import WriteConcern
from typing import Any, Optional, Union

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from typing_extensions import Protocol, runtime_checkable

ReadPreferences = Union[Primary, PrimaryPreferred, Secondary, SecondaryPreferred, Nearest]

@runtime_checkable
class DummyMongoClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def get_database(
        self,
        name: Optional[str] = None,
        *,
        codec_options: Optional[CodecOptions] = None,
        read_preference: Optional[ReadPreferences] = None,
        write_concern: Optional[WriteConcern] = None,
        read_concern: Optional[ReadConcern] = None,
    ):
        raise NotImplementedError
    
    async def start_session(
        self,
        *,
        causal_consistency: Optional[bool] = None,
        default_transaction_options: Optional[TransactionOptions] = None,
        snapshot: bool = False,
    ):
        raise NotImplementedError

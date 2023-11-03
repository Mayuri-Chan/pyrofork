from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import pyrogram
from pyrogram import filters

from .identifier import Identifier
from .listener_types import ListenerTypes


@dataclass
class Listener:
    listener_type: ListenerTypes
    filters: "pyrogram.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None

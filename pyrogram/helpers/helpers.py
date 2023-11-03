from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)


def ikb(rows=None):
    """
    Create an InlineKeyboardMarkup from a list of lists of buttons.
    :param rows: List of lists of buttons. Defaults to empty list.
    :return: InlineKeyboardMarkup
    """
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            button = (
                btn(button, button) if isinstance(button, str) else btn(*button)
            )  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)
    # return {'inline_keyboard': lines}


def btn(text, value, type="callback_data"):
    """
    Create an InlineKeyboardButton.

    :param text: Text of the button.
    :param value: Value of the button.
    :param type: Type of the button. Defaults to "callback_data".
    :return: InlineKeyboardButton
    """
    return InlineKeyboardButton(text, **{type: value})
    # return {'text': text, type: value}


# The inverse of above
def bki(keyboard):
    """
    Create a list of lists of buttons from an InlineKeyboardMarkup.

    :param keyboard: InlineKeyboardMarkup
    :return: List of lists of buttons
    """
    lines = []
    for row in keyboard.inline_keyboard:
        line = []
        for button in row:
            button = ntb(button)  # btn() format
            line.append(button)
        lines.append(line)
    return lines
    # return ikb() format


def ntb(button):
    """
    Create a button list from an InlineKeyboardButton.

    :param button: InlineKeyboardButton
    :return: Button as a list to be used in btn()
    """
    for btn_type in [
        "callback_data",
        "url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
    ]:
        value = getattr(button, btn_type)
        if value:
            break
    button = [button.text, value]
    if btn_type != "callback_data":
        button.append(btn_type)
    return button
    # return {'text': text, type: value}


def kb(rows=None, **kwargs):
    """
    Create a ReplyKeyboardMarkup from a list of lists of buttons.

    :param rows: List of lists of buttons. Defaults to empty list.
    :param kwargs: Other arguments to pass to ReplyKeyboardMarkup.
    :return: ReplyKeyboardMarkup
    """
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            button_type = type(button)
            if button_type == str:
                button = KeyboardButton(button)
            elif button_type == dict:
                button = KeyboardButton(**button)

            line.append(button)
        lines.append(line)
    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


kbtn = KeyboardButton
"""
Create a KeyboardButton.
"""


def force_reply(selective=True):
    """
    Create a ForceReply.

    :param selective: Whether the reply should be selective. Defaults to True.
    :return: ForceReply
    """
    return ForceReply(selective=selective)


def array_chunk(input_array, size):
    """
    Split an array into chunks.

    :param input_array: The array to split.
    :param size: The size of each chunk.
    :return: List of chunks.
    """
    return [input_array[i: i + size] for i in range(0, len(input_array), size)]

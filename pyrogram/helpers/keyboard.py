

from pyrogram.emoji import *
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply)
from typing import List, Union


class InlineKeyboard(InlineKeyboardMarkup):
    _SYMBOL_FIRST_PAGE = '« {}'
    _SYMBOL_PREVIOUS_PAGE = '‹ {}'
    _SYMBOL_CURRENT_PAGE = '· {} ·'
    _SYMBOL_NEXT_PAGE = '{} ›'
    _SYMBOL_LAST_PAGE = '{} »'
    _LOCALES = {
        'be_BY': f'{FLAG_BELARUS} Беларуская',          # Belarusian - Belarus
        'de_DE': f'{FLAG_GERMANY} Deutsch',             # German - Germany
        'zh_CN': f'{FLAG_CHINA} 中文',                  # Chinese - China
        # English - United States
        'en_US': f'{FLAG_UNITED_KINGDOM}  English',
        'fr_FR': f'{FLAG_FRANCE} Français',             # French - France
        # Indonesian - Indonesia
        'id_ID': f'{FLAG_INDONESIA} Bahasa Indonesia',
        'it_IT': f'{FLAG_ITALY} Italiano',              # Italian - Italy
        'ko_KR': f'{FLAG_SOUTH_KOREA} 한국어',          # Korean - Korea
        'tr_TR': f'{FLAG_TURKEY} Türkçe',               # Turkish - Turkey
        'ru_RU': f'{FLAG_RUSSIA} Русский',              # Russian - Russia
        'es_ES': f'{FLAG_SPAIN} Español',               # Spanish - Spain
        'uk_UA': f'{FLAG_UKRAINE} Українська',          # Ukrainian - Ukraine
        'uz_UZ': f'{FLAG_UZBEKISTAN} Oʻzbekcha',        # Uzbek - Uzbekistan
    }

    def __init__(self, row_width=3):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.row_width = row_width

    def add(self, *args):
        self.inline_keyboard = [
            args[i:i + self.row_width]
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args):
        self.inline_keyboard.append([button for button in args])

    def _add_button(self, text, callback_data):
        return InlineKeyboardButton(
            text=text,
            callback_data=self.callback_pattern.format(
                number=callback_data)
        )

    @property
    def _left_pagination(self):
        return [
            self._add_button(
                self._SYMBOL_CURRENT_PAGE.format(number), number)
            if number == self.current_page else self._add_button(
                self._SYMBOL_NEXT_PAGE.format(number), number)
            if number == 4 else self._add_button(
                self._SYMBOL_LAST_PAGE.format(self.count_pages),
                self.count_pages)
            if number == 5 else self._add_button(number, number)
            for number in range(1, 6)
        ]

    @property
    def _middle_pagination(self):
        return [
            self._add_button(
                self._SYMBOL_FIRST_PAGE.format(1), 1),
            self._add_button(
                self._SYMBOL_PREVIOUS_PAGE.format(self.current_page - 1),
                self.current_page - 1),
            self._add_button(
                self._SYMBOL_CURRENT_PAGE.format(self.current_page),
                self.current_page),
            self._add_button(
                self._SYMBOL_NEXT_PAGE.format(self.current_page + 1),
                self.current_page + 1),
            self._add_button(
                self._SYMBOL_LAST_PAGE.format(self.count_pages),
                self.count_pages)
        ]

    @property
    def _right_pagination(self):
        return [
            self._add_button(
                self._SYMBOL_FIRST_PAGE.format(1), 1),
            self._add_button(
                self._SYMBOL_PREVIOUS_PAGE.format(self.count_pages - 3),
                self.count_pages - 3)
        ] + [
            self._add_button(
                self._SYMBOL_CURRENT_PAGE.format(number), number)
            if number == self.current_page else self._add_button(number, number)
            for number in range(self.count_pages - 2, self.count_pages + 1)
        ]

    @property
    def _full_pagination(self):
        return [
            self._add_button(number, number)
            if number != self.current_page else self._add_button(
                self._SYMBOL_CURRENT_PAGE.format(number), number)
            for number in range(1, self.count_pages + 1)
        ]

    @property
    def _build_pagination(self):
        if self.count_pages <= 5:
            return self._full_pagination
        else:
            if self.current_page <= 3:
                return self._left_pagination
            elif self.current_page > self.count_pages - 3:
                return self._right_pagination
            else:
                return self._middle_pagination

    def paginate(self, count_pages: int, current_page: int,
                 callback_pattern: str):
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern

        return self.inline_keyboard.append(self._build_pagination)

    def languages(self, callback_pattern: str, locales: Union[str, List[str]],
                  row_width: int = 2):
        locales = locales if isinstance(locales, list) else [locales]

        buttons = [
            InlineKeyboardButton(
                text=self._LOCALES.get(locales[i], 'Invalid locale'),
                callback_data=callback_pattern.format(locale=locales[i])
            )
            for i in range(0, len(locales))
        ]

        self.inline_keyboard = [
            buttons[i:i + row_width]
            for i in range(0, len(buttons), row_width)
        ]


class InlineButton(InlineKeyboardButton):
    def __init__(self, text=None, callback_data=None, url=None,
                 login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            login_url=login_url,
            user_id=user_id,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            callback_game=callback_game
        )


class InlinePaginationKeyboard(InlineKeyboardMarkup):
    SYMBOL_FIRST_PAGE = '« {}'
    SYMBOL_PREVIOUS_PAGE = '‹ {}'
    SYMBOL_CURRENT_PAGE = '· {} ·'
    SYMBOL_NEXT_PAGE = '{} ›'
    SYMBOL_LAST_PAGE = '{} »'

    def __init__(self, count_pages: int, current_page: int,
                 callback_pattern: str):
        self.inline_keyboard = list()
        super().__init__(inline_keyboard=self.inline_keyboard)
        self.count_pages = count_pages
        self.current_page = current_page
        self.callback_pattern = callback_pattern
        self.markup

    def add_button(self, text, callback_data):
        return InlineKeyboardButton(
            text=text,
            callback_data=self.callback_pattern.format(
                number=callback_data)
        )

    @property
    def left_pagination(self):
        return [
            self.add_button(
                self.SYMBOL_CURRENT_PAGE.format(number), number)
            if number == self.current_page else self.add_button(
                self.SYMBOL_NEXT_PAGE.format(number), number)
            if number == 4 else self.add_button(
                self.SYMBOL_LAST_PAGE.format(self.count_pages),
                self.count_pages)
            if number == 5 else self.add_button(number, number)
            for number in range(1, 6)
        ]

    @property
    def middle_pagination(self):
        return [
            self.add_button(
                self.SYMBOL_FIRST_PAGE.format(1), 1),
            self.add_button(
                self.SYMBOL_PREVIOUS_PAGE.format(self.current_page - 1),
                self.current_page - 1),
            self.add_button(
                self.SYMBOL_CURRENT_PAGE.format(self.current_page),
                self.current_page),
            self.add_button(
                self.SYMBOL_NEXT_PAGE.format(self.current_page + 1),
                self.current_page + 1),
            self.add_button(
                self.SYMBOL_LAST_PAGE.format(self.count_pages),
                self.count_pages),
        ]

    @property
    def right_pagination(self):
        return [
            self.add_button(
                self.SYMBOL_FIRST_PAGE.format(1), 1),
            self.add_button(
                self.SYMBOL_PREVIOUS_PAGE.format(self.count_pages - 3),
                self.count_pages - 3)
        ] + [
            self.add_button(
                self.SYMBOL_CURRENT_PAGE.format(number), number)
            if number == self.current_page else self.add_button(number, number)
            for number in range(self.count_pages - 2, self.count_pages + 1)
        ]

    @property
    def full_pagination(self):
        return [
            self.add_button(number, number)
            if number != self.current_page else self.add_button(
                self.SYMBOL_CURRENT_PAGE.format(number), number)
            for number in range(1, self.count_pages + 1)
        ]

    @property
    def build_pagination(self):
        if self.count_pages <= 5:
            return self.full_pagination
        else:
            if self.current_page <= 3:
                return self.left_pagination
            elif self.current_page > self.count_pages - 3:
                return self.right_pagination
            else:
                return self.middle_pagination

    def row(self, *args):
        self.inline_keyboard.append([button for button in args])

    @property
    def markup(self):
        self.inline_keyboard.append(self.build_pagination)


class InlineButton(InlineKeyboardButton):
    def __init__(self, text=None, callback_data=None, url=None,
                 login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None):
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            login_url=login_url,
            user_id=user_id,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            callback_game=callback_game
        )


class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=None, one_time_keyboard=None,
                 selective=None, placeholder=None, row_width=3):
        self.keyboard = list()
        super().__init__(
            keyboard=self.keyboard,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            placeholder=placeholder
        )
        self.row_width = row_width

    def add(self, *args):
        self.keyboard = [
            args[i:i + self.row_width]
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args):
        self.keyboard.append([button for button in args])


class ReplyButton(KeyboardButton):
    def __init__(self, text=None, request_contact=None, request_location=None):
        super().__init__(
            text=text,
            request_contact=request_contact,
            request_location=request_location
        )


class ReplyKeyboardRemove(ReplyKeyboardRemove):
    def __init__(self, selective=None):
        super().__init__(selective=selective)


class ForceReply(ForceReply):
    def __init__(self, selective=None, placeholder=None):
        super().__init__(selective=selective, placeholder=placeholder)

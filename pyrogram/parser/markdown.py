#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import html
import logging
import re
from typing import Optional

import pyrogram
from pyrogram.enums import MessageEntityType
from . import utils
from .html import HTML

BOLD_DELIM = "**"
ITALIC_DELIM = "__"
UNDERLINE_DELIM = "--"
STRIKE_DELIM = "~~"
SPOILER_DELIM = "||"
CODE_DELIM = "`"
PRE_DELIM = "```"
BLOCKQUOTE_DELIM = ">"
BLOCKQUOTE_EXPANDABLE_DELIM = "**>"

MARKDOWN_RE = re.compile(r"({d})".format(
    d="|".join(
        ["".join(i) for i in [
            [rf"\{j}" for j in i]
            for i in [
                PRE_DELIM,
                CODE_DELIM,
                STRIKE_DELIM,
                UNDERLINE_DELIM,
                ITALIC_DELIM,
                BOLD_DELIM,
                SPOILER_DELIM
            ]
        ]]
    )))
URL_RE = re.compile(r"(!?)\[(.+?)\]\((.+?)\)")

OPENING_TAG = "<{}>"
CLOSING_TAG = "</{}>"
URL_MARKUP = '<a href="{}">{}</a>'
EMOJI_MARKUP = '<emoji id={}>{}</emoji>'
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]
CODE_TAG_RE = re.compile(r"<code>.*?</code>")


class Markdown:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.html = HTML(client)

    def blockquote_parser(self, text):
        text = re.sub(r'\n&gt;', '\n>', re.sub(r'^&gt;', '>', text))
        lines = text.split('\n')
        result = []

        in_blockquote = False

        for line in lines:
            if line.startswith(BLOCKQUOTE_DELIM):
                if not in_blockquote:
                    line = re.sub(r'^> ', OPENING_TAG.format("blockquote"), line)
                    line = re.sub(r'^>', OPENING_TAG.format("blockquote"), line)
                    in_blockquote = True
                    result.append(line.strip())
                else:
                    result.append(line[1:].strip())
            elif line.startswith(BLOCKQUOTE_EXPANDABLE_DELIM):
                if not in_blockquote:
                    line = re.sub(r'^\*\*> ', OPENING_TAG.format("blockquote expandable"), line)
                    line = re.sub(r'^\*\*>', OPENING_TAG.format("blockquote expandable"), line)
                    in_blockquote = True
                    result.append(line.strip())
                else:
                    result.append(line[3:].strip())
            else:
                if in_blockquote:
                    line = CLOSING_TAG.format("blockquote") + line
                    in_blockquote = False
                result.append(line)

        if in_blockquote:
            line = result[len(result)-1] + CLOSING_TAG.format("blockquote")
            result.pop(len(result)-1)
            result.append(line)

        return '\n'.join(result)

    async def parse(self, text: str, strict: bool = False):
        if strict:
            text = html.escape(text)
        text = self.blockquote_parser(text)

        delims = set()
        is_fixed_width = False

        placeholders = {}
        for i, code_section in enumerate(CODE_TAG_RE.findall(text)):
            placeholder = f"{{CODE_SECTION_{i}}}"
            placeholders[placeholder] = code_section
            text = text.replace(code_section, placeholder, 1)

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim = match.group(1)
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if delim == BOLD_DELIM:
                tag = "b"
            elif delim == ITALIC_DELIM:
                tag = "i"
            elif delim == UNDERLINE_DELIM:
                tag = "u"
            elif delim == STRIKE_DELIM:
                tag = "s"
            elif delim == CODE_DELIM:
                tag = "code"
            elif delim == PRE_DELIM:
                tag = "pre"
            elif delim == SPOILER_DELIM:
                tag = "spoiler"
            else:
                continue

            if delim not in delims:
                delims.add(delim)
                tag = OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = CLOSING_TAG.format(tag)

            if delim == PRE_DELIM and delim in delims:
                delim_and_language = text[text.find(PRE_DELIM):].split("\n")[0]
                language = delim_and_language[len(PRE_DELIM):]
                text = utils.replace_once(text, delim_and_language, f'<pre language="{language}">', start)
                continue

            text = utils.replace_once(text, delim, tag, start)

        for i, match in enumerate(re.finditer(URL_RE, text)):
            start, _ = match.span()
            is_emoji, text_url, url = match.groups()
            full = match.group(0)

            if not is_emoji and text_url:
                text = utils.replace_once(text, full, URL_MARKUP.format(url, text_url), start)
                continue

            if is_emoji:
                emoji = text_url
                emoji_id = url.lstrip("tg://emoji?id=")
                text = utils.replace_once(text, full, EMOJI_MARKUP.format(emoji_id, emoji), start)
                continue

        for placeholder, code_section in placeholders.items():
            text = text.replace(placeholder, code_section)

        return await self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list):
        """
        Performs the reverse operation to .parse(), effectively returning
        markdown-like syntax given a normal text and its MessageEntity's.

        :param text: the text to be reconverted into markdown.
        :param entities: list of MessageEntity's applied to the text.
        :return: a markdown-like text representing the combination of both inputs.
        """
        delimiters = {
            MessageEntityType.BOLD: BOLD_DELIM,
            MessageEntityType.ITALIC: ITALIC_DELIM,
            MessageEntityType.UNDERLINE: UNDERLINE_DELIM,
            MessageEntityType.STRIKETHROUGH: STRIKE_DELIM,
            MessageEntityType.CODE: CODE_DELIM,
            MessageEntityType.PRE: PRE_DELIM,
            MessageEntityType.BLOCKQUOTE: BLOCKQUOTE_DELIM,
            MessageEntityType.EXPANDABLE_BLOCKQUOTE: BLOCKQUOTE_EXPANDABLE_DELIM,
            MessageEntityType.SPOILER: SPOILER_DELIM
        }

        text = utils.add_surrogates(text)

        insert_at = []
        for i, entity in enumerate(entities):
            s = entity.offset
            e = entity.offset + entity.length
            delimiter = delimiters.get(entity.type, None)
            if delimiter:
                if entity.type == MessageEntityType.PRE:
                    inside_blockquote = any(
                        blk_entity.offset <= s < blk_entity.offset + blk_entity.length and
                        blk_entity.offset < e <= blk_entity.offset + blk_entity.length
                        for blk_entity in entities
                        if blk_entity.type == MessageEntityType.BLOCKQUOTE
                    )
                    is_expandable = any(
                        blk_entity.offset <= s < blk_entity.offset + blk_entity.length and
                        blk_entity.offset < e <= blk_entity.offset + blk_entity.length and
                        blk_entity.collapsed
                        for blk_entity in entities
                        if blk_entity.type == MessageEntityType.BLOCKQUOTE
                    )
                    if inside_blockquote:
                        if is_expandable:
                            if entity.language:
                                open_delimiter = f"{delimiter}{entity.language}\n**>"
                            else:
                                open_delimiter = f"{delimiter}\n**>"
                            close_delimiter = f"\n**>{delimiter}"
                        else:
                            if entity.language:
                                open_delimiter = f"{delimiter}{entity.language}\n>"
                            else:
                                open_delimiter = f"{delimiter}\n>"
                            close_delimiter = f"\n>{delimiter}"
                    else:
                        open_delimiter = delimiter
                        close_delimiter = delimiter
                    insert_at.append((s, i, open_delimiter))
                    insert_at.append((e, -i, close_delimiter))
                elif entity.type != MessageEntityType.BLOCKQUOTE and entity.type != MessageEntityType.EXPANDABLE_BLOCKQUOTE:
                    open_delimiter = delimiter
                    close_delimiter = delimiter
                    insert_at.append((s, i, open_delimiter))
                    insert_at.append((e, -i, close_delimiter))
                else:
                    # Handle multiline blockquotes
                    text_subset = text[s:e]
                    lines = text_subset.splitlines()
                    for line_num, line in enumerate(lines):
                        line_start = s + sum(len(l) + 1 for l in lines[:line_num])
                        if entity.collapsed:
                            insert_at.append((line_start, i, BLOCKQUOTE_EXPANDABLE_DELIM))
                        else:
                            insert_at.append((line_start, i, BLOCKQUOTE_DELIM))
                    # No closing delimiter for blockquotes
            else:
                url = None
                is_emoji = False
                if entity.type == MessageEntityType.TEXT_LINK:
                    url = entity.url
                elif entity.type == MessageEntityType.TEXT_MENTION:
                    url = f'tg://user?id={entity.user.id}'
                elif entity.type == MessageEntityType.CUSTOM_EMOJI:
                    url = f"tg://emoji?id={entity.custom_emoji_id}"
                    is_emoji = True
                if url:
                    if is_emoji:
                        insert_at.append((s, i, '!['))
                    else:
                        insert_at.append((s, i, '['))
                    insert_at.append((e, -i, f']({url})'))

        insert_at.sort(key=lambda t: (t[0], t[1]))
        while insert_at:
            at, _, what = insert_at.pop()

            # If we are in the middle of a surrogate nudge the position by -1.
            # Otherwise we would end up with malformed text and fail to encode.
            # For example of bad input: "Hi \ud83d\ude1c"
            # https://en.wikipedia.org/wiki/UTF-16#U+010000_to_U+10FFFF
            while utils.within_surrogate(text, at):
                at += 1

            text = text[:at] + what + text[at:]

        return utils.remove_surrogates(text)

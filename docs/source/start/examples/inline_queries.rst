inline_queries
==============

This example shows how to handle inline queries.

Two results are generated when users invoke the bot inline mode, e.g.: @pyrogrambot hi.
It uses the @on_inline_query decorator to register an InlineQueryHandler.

.. code-block:: python

    from pyrogram import Client
    from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                                InlineKeyboardMarkup, InlineKeyboardButton)

    app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


    @app.on_inline_query()
    async def answer(client, inline_query):
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Installation",
                    input_message_content=InputTextMessageContent(
                        "Here's how to install **Pyrofork**"
                    ),
                    url="https://pyrofork.mayuri.my.id/intro/install",
                    description="How to install Pyrofork",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "Open website",
                                url="https://pyrofork.mayuri.my.id/intro/install"
                            )]
                        ]
                    )
                ),
                InlineQueryResultArticle(
                    title="Usage",
                    input_message_content=InputTextMessageContent(
                        "Here's how to use **Pyrofork**"
                    ),
                    url="https://pyrofork.mayuri.my.id/start/invoking",
                    description="How to use Pyrofork",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "Open website",
                                url="https://pyrofork.mayuri.my.id/start/invoking"
                            )]
                        ]
                    )
                )
            ],
            cache_time=1
        )


    app.run()  # Automatically start() and idle()
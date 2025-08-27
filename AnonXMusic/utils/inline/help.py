from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AnonXMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
    ]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["z1_xa"],
                    callback_data="help_callback hb1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["z1_xa"],
                    callback_data="help_callback hb2",                                
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["z1_xa"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons

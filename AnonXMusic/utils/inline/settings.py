from typing import Union

from pyrogram.types import InlineKeyboardButton


def setting_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="AU"),       
        ],
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="PM"),
        ],
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="VM"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="وضع التصويت ➜", callback_data="VOTEANSWER"),
            InlineKeyboardButton(
                text=_["z1_xa"] if mode == True else _["z1_xa"],
                callback_data="VOMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M"),
            InlineKeyboardButton(
                text=f"حالياً : {current}",
                callback_data="ANSWERVOMODE",
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A"),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text=_["z1_xa"] if status == True else _["z1_xa"],
                callback_data="AUTH",
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST"),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text=_["z1_xa"] if Direct == True else _["z1_xa"],
                callback_data="MODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text=_["z1_xa"] if Group == True else _["z1_xa"],
                callback_data="CHANNELMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text=_["z1_xa"], callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(
                text=_["z1_xa"] if Playtype == True else _["z1_xa"],
                callback_data="PLAYTYPECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons

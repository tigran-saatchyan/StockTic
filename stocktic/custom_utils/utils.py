"""This module provides utility functions for the Django project, including
functions for saving pictures and formatting market capitalization values.

Functions:
    save_picture: Saves a picture with a formatted filename based on the
        instance and current date.
    format_market_cap: Formats a market capitalization value into a h
        uman-readable string with appropriate units (K, M, B, T).
"""

from datetime import datetime


def save_picture(instance, filename):
    """Saves a picture with a formatted filename based on the instance
    and current date.

    Args:
        instance: The model instance to which the picture belongs.
        filename (str): The original filename of the picture.

    Returns:
        str: The formatted filename for saving the picture.
    """
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name

    raw_date = datetime.now()
    formatted_date = raw_date.strftime("%Y-%m-%d %H:%M:%S")

    picture_name = "".join(
        [
            "".join(filename.split(".")[:-1]),
            formatted_date,
            ".",
            filename.split(".")[-1],
        ]
    )
    return (
        f"{app_name}/{model_name}/{instance.pk}/{instance.pk}_"
        f"{picture_name}"
    )


def format_market_cap(value):
    """Formats a market capitalization value into a human-readable
    string with appropriate units (K, M, B, T).

    Args:
        value (float): The market capitalization value to format.

    Returns:
        str: The formatted market capitalization value.
    """
    trillion = 1_000_000_000_000
    billion = 1_000_000_000
    million = 1_000_000
    thousand = 1_000

    value = float(value) if value else 0

    if value >= trillion:
        return f"{value / trillion:.2f}T"

    if value >= billion:
        return f"{value / billion:.2f}B"

    if value >= million:
        return f"{value / million:.2f}M"

    if value >= thousand:
        return f"{value / thousand:.2f}K"

    return str(value)

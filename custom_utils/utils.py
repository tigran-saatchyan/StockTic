from datetime import datetime


def save_picture(instance, filename):
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
    return f"{app_name}/{model_name}/{instance.pk}/{instance.pk}_" f"{picture_name}"


def format_market_cap(value):
    trillion = 1_000_000_000_000
    billion = 1_000_000_000
    million = 1_000_000
    thousand = 1_000

    value = float(value) if value else 0

    if value >= trillion:
        return f"{value / trillion:.2f}T"
    elif value >= billion:
        return f"{value / billion:.2f}B"
    elif value >= million:
        return f"{value / million:.2f}M"
    elif value >= thousand:
        return f"{value / thousand:.2f}K"
    else:
        return str(value)

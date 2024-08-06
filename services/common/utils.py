def format_market_cap(value):
    trillion = 1_000_000_000_000
    billion = 1_000_000_000
    million = 1_000_000

    if value >= trillion:
        return f'{value / trillion:.3f}T'
    elif value >= billion:
        return f'{value / billion:.3f}B'
    elif value >= million:
        return f'{value / million:.3f}M'
    else:
        return str(value)

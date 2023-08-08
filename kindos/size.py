def human_readable_size(size: int) -> str:
    """Returns human readable size"""
    if size < 1024:
        return f"{size}B"
    size /= 1024
    if size < 1024:
        return f"{size:.2f}KB"
    size /= 1024
    if size < 1024:
        return f"{size:.2f}MB"
    size /= 1024
    return f"{size:.2f}GB"

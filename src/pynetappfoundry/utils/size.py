"""Convert file sizes to human-readable form.

Available functions:
    approximate_size(size, a_kilobyte_is_1024_bytes)
        takes a file size and returns a human-readable string

Examples:
    >>> approximate_size(1024)
    '1.0 KiB'
    >>> approximate_size(1000, False)
    '1.0 KB'
"""

from __future__ import annotations

SUFFIXES: dict[int, list[str]] = {
    1000: ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
    1024: ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"],
}


def approximate_size(
    size: int | float,
    a_kilobyte_is_1024_bytes: bool = True,
    newsuffix: str | None = None,
    withsuffix: bool = True,
) -> str | float:
    """Convert a file size to human-readable form.

    Args:
        size: File size in bytes.
        a_kilobyte_is_1024_bytes: If True (default), use multiples of 1024.
                                  If False, use multiples of 1000.
        newsuffix: If provided, convert to this specific suffix.
        withsuffix: If True (default), include suffix in result.

    Returns:
        Human-readable size string, or float if withsuffix is False.

    Raises:
        ValueError: If size is negative or too large.
    """
    if size < 0:
        raise ValueError("number must be non-negative")

    if newsuffix:
        return approximate_size_specific(size, newsuffix, withsuffix)

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            if withsuffix:
                return f"{size:.2f} {suffix}"
            else:
                return size

    raise ValueError("number too large")


def approximate_size_specific(
    size: int | float, newsuffix: str, withsuffix: bool = True
) -> str | float:
    """Convert a size in bytes to a specific suffix (like GB, TB, TiB).

    Args:
        size: Size in bytes.
        newsuffix: Target suffix (e.g., 'GB', 'TiB').
        withsuffix: If True, include suffix in result.

    Returns:
        Converted size as string with suffix, float without, or -1 if suffix not found.
    """
    for multiple in SUFFIXES:
        for suffix in SUFFIXES[multiple]:
            if suffix.lower() == newsuffix.lower():
                power = SUFFIXES[multiple].index(suffix)
                newsizeint = float(size) / (multiple ** float(power + 1))
                if withsuffix:
                    return f"{newsizeint:.2f} {suffix}"
                else:
                    return newsizeint

    return -1


def convert_size(dsize: str, newsuffix: str, withsuffix: bool = True) -> str | float:
    """Convert a file size like 8TB to another size.

    Args:
        dsize: Size string with suffix (e.g., '8TB').
        newsuffix: The suffix to convert to.
        withsuffix: If True, return size with new suffix; otherwise just the number.

    Returns:
        Converted size.
    """
    newsize: float = 0
    foundmult: int = 0
    power: int = 0
    foundsuffix: str = ""

    for multiple in SUFFIXES:
        for suffix in SUFFIXES[multiple]:
            if suffix in dsize:
                foundmult = multiple
                foundsuffix = suffix
                power = SUFFIXES[multiple].index(suffix) + 1
                size_str = dsize.replace(foundsuffix, "").strip()
                size_val = float(size_str)
                newsize = size_val * (foundmult**power)

    newsizes = approximate_size_specific(newsize, newsuffix)

    if withsuffix:
        return newsizes

    else:
        if isinstance(newsizes, str):
            return float(newsizes.replace(newsuffix, ""))
        return newsizes


if __name__ == "__main__":
    print(approximate_size(1000000000000, False))
    print(approximate_size(1000000000000))

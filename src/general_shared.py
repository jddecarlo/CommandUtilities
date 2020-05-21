"""A shared library of classes and functions useful for many different applications."""

def fix_path_seperators(path):
    """Replaces unix-style path seperators with Windows-style path seperators.

    Args:
        path: A path string to check for unix-style path seperators.
    Returns:
        The given path with the seperators fixed."""
    return path.replace('/', '\\') if path is not None else ''

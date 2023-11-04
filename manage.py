#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from typing import Final


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        IMPORT_ERROR_MESSAGE: Final[str] = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(IMPORT_ERROR_MESSAGE) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

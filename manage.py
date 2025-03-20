#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def main():
    """Run administrative tasks."""
    DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{DJANGO_ENV}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

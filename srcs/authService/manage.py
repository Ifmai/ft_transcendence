#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from cryptography.fernet import Fernet

def create_key_if_not_exists():
    key_file = 'secret.key'
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as key_file:
            key_file.write(key)
        os.environ['FERNET_KEY'] = key.decode()
    else:
        with open(key_file, 'rb') as key_file:
            key = key_file.read()
        os.environ['FERNET_KEY'] = key.decode()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authService.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    create_key_if_not_exists()
    main()

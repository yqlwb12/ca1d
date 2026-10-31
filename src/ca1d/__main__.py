"""Allow ``python -m ca1d``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

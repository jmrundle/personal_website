#!/usr/bin/env python3
from personal_site import build_app
import sys


def usage(status):
    print("Usage: ./run.py [PORT]")
    sys.exit(status)


def main():
    if len(sys.argv) < 2:
        usage(1)

    app  = build_app()
    port = sys.argv[1]
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()

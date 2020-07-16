#!/usr/bin/env python3
from personal_site import build_app
import sys


PROG_NAME = sys.argv[0]


def usage(status):
    print(f"Usage: {PROG_NAME} [PORT] [-d]")
    sys.exit(status)


def main():
    if len(sys.argv) < 2:
        usage(1)

    port = sys.argv[1]
    debug = len(sys.argv) > 2 and sys.argv[2] == '-d'

    app = build_app(debug)

    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

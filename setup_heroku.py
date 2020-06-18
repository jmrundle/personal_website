#!/usr/bin/env python3
import os
import sys
from config import Config


def env_vars():
    env_file   = Config.ENV_FILE
    declarations = ""

    if not os.path.exists(env_file):
        print("Hey, you need a .env file.", file=sys.stderr)
        sys.exit(1)

    with open(env_file, 'r') as env:
        for line in env.readlines():
            declarations += line.rstrip() + ' '

    return declarations


def set_heroku_config(declarations):
    os.system(f"heroku config:set {declarations}")


def main():
    declarations = env_vars()
    set_heroku_config(declarations)


if __name__ == "__main__":
    main()

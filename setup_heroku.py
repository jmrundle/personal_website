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


def spotipy_cache_var():
    cache_file = Config.SPOTIFY_CACHE_PATH

    if not os.path.exists(cache_file):
        print("Hey, you need to run setup_spotify.py", file=sys.stderr)
        sys.exit(2)

    with open(cache_file, 'r') as cache:
        token_info = cache.read()
        declaration = f"SPOTIPY_CACHE='{token_info}'"

    return declaration


def set_heroku_config(declarations):
    os.system(f"heroku config:set {declarations}")


def main():
    declarations = ""
    declarations += env_vars()
    declarations += spotipy_cache_var()
    set_heroku_config(declarations)

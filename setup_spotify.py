#!/usr/bin/env python3

import sys
import spotipy
from config import Config


def main():
    env_file      = Config.ENV_FILE
    client_id     = Config.SPOTIFY_CLIENT_ID
    client_secret = Config.SPOTIFY_CLIENT_SECRET
    redirect_uri  = Config.SPOTIFY_REDIRECT_URI
    cache_path    = Config.SPOTIFY_CACHE_PATH
    scopes        = Config.SPOTIFY_SCOPES

    if not client_id or not client_secret or not redirect_uri:
        print(f"""
        configure the following variables in {env_file}
        or set them as env variables manually:
        
        export SPOTIFY_CLIENT_ID=...
        export SPOTIFY_CLIENT_SECRET=...
        export SPOTIFY_REDIRECT_URI=...
        """)
        sys.exit(1)

    oauth_manager = spotipy.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        cache_path=cache_path,
        scope=scopes
    )

    code = oauth_manager.get_auth_response()
    oauth_manager.get_access_token(code, as_dict=False, check_cache=False)

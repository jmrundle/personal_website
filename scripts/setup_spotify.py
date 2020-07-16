#!/usr/bin/env python3

import sys
import spotipy
from config.app_config import BaseConfig


def main():
    env_file      = BaseConfig.ENV_FILE
    client_id     = BaseConfig.SPOTIFY_CLIENT_ID
    client_secret = BaseConfig.SPOTIFY_CLIENT_SECRET
    redirect_uri  = BaseConfig.SPOTIFY_REDIRECT_URI
    cache_path    = BaseConfig.SPOTIFY_CACHE_PATH
    scopes        = BaseConfig.SPOTIFY_SCOPES

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


if __name__ == "__main__":
    main()

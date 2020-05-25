import os
import sys
import time
import requests
import spotipy


class ApiServices:
    def __init__(self, app):
        self.github  = Github(
            username=app.config["GITHUB_USERNAME"],
            access_token=app.config["GITHUB_ACCESS_TOKEN"]
        )
        self.spotify = Spotify(
            client_id=app.config["SPOTIFY_CLIENT_ID"],
            client_secret=app.config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=app.config["SPOTIFY_REDIRECT_URI"],
            cache_path=app.config["SPOTIFY_CACHE_PATH"]
        )

        self.refresh_period = int(app.config["API_REFRESH_PERIOD"])
        self.last_refresh   = 0
        self.refresh()

    def refresh(self):
        now = time.time()

        if (now - self.last_refresh) > self.refresh_period:
            print("Making requests!")
            try:
                self.github.refresh()
                self.spotify.refresh()
            except requests.exceptions.ConnectionError:
                pass

            self.last_refresh = now


class Github:
    API_PREFIX = "https://api.github.com"

    def __init__(self, username, access_token):
        self.username     = username
        self.access_token = access_token
        self.profile      = []
        self.events       = []

    def refresh(self):
        self.profile = self._profile()
        self.events  = self._events()

    def _request(self, url):
        headers = {
            "Authorization": f"{self.username}:{self.access_token}"
        }
        resp = requests.get(url, headers=headers)
        if not resp.ok:
            return {}
        return resp.json()

    def _profile(self):
        url = f"{self.API_PREFIX}/users/{self.username}"
        return self._request(url)

    def _events(self):
        url = f"{self.API_PREFIX}/users/{self.username}/events"
        requests.get(url)
        return self._request(url)[:10]


class Spotify:
    def __init__(self, client_id, client_secret, redirect_uri, cache_path):
        oauth_manager = spotipy.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            cache_path=cache_path,
            scope="user-top-read"
        )

        # make sure cache file exists
        if not os.path.exists(cache_path):
            print("Need to generate Spotify API token first. Run setup_spotify.py.", sys.stderr)
            sys.exit(1)

        self.wrapper     = spotipy.Spotify(oauth_manager=oauth_manager)
        self.top_artists = []
        self.top_tracks  = []

    def refresh(self):
        self.top_artists = self._top_artists()
        self.top_tracks  = self._top_tracks()

    def _top_artists(self):
        return self.wrapper.current_user_top_artists(limit=8, time_range="short_term")

    def _top_tracks(self):
        return self.wrapper.current_user_top_tracks(limit=8, time_range="short_term")

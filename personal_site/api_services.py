import os
import sys
import time
import json
import requests
import spotipy
import boto3
from .oauth2 import SpotifyOAuth as WaitingForPyPiUpdateSpotifyOAuth


class ApiServices:
    def __init__(self, app):
        self.github  = Github(
            username=app.config["INSTANCE_INFO"]["social_usernames"]["github"],
            access_token=app.config["GITHUB_ACCESS_TOKEN"]
        )
        self.spotify = Spotify(
            client_id=app.config["SPOTIFY_CLIENT_ID"],
            client_secret=app.config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=app.config["SPOTIFY_REDIRECT_URI"],
            cache_path=app.config["SPOTIFY_CACHE_PATH"],
            scopes=app.config["SPOTIFY_SCOPES"],
            s3_bucket=app.config["S3_BUCKET"],
            s3_cache_file=app.config["S3_CACHE_FILE"]
        )

        self.services       = [self.spotify, self.github]
        self.refresh_period = int(app.config["API_REFRESH_PERIOD"])
        self.last_refresh   = 0
        self.refresh()

    def refresh(self):
        now = time.time()

        if (now - self.last_refresh) > self.refresh_period:
            print("Making requests!")

            for service in self.services:
                service.refresh()

            self.last_refresh = now


class ApiObject:
    def refresh(self):
        raise NotImplementedError


class Github(ApiObject):
    API_PREFIX = "https://api.github.com"
    EVENT_COUNT = 10

    def __init__(self, username, access_token):
        self.username     = username
        self.access_token = access_token
        self.profile      = []
        self.events       = []

    def refresh(self):
        try:
            self.profile = self._profile()
            self.events = self._events()
        except requests.exceptions.ConnectionError:
            pass

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
        return self._request(url)[:self.EVENT_COUNT]


class Spotify(ApiObject):
    TOP_LIMIT = 8

    def __init__(self, client_id, client_secret, redirect_uri, cache_path, scopes, s3_bucket, s3_cache_file):
        oauth_manager = SpotifyOAuthWithS3Cache(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            cache_path=cache_path,
            scope=scopes,
            s3_bucket=s3_bucket,
            s3_cache_file=s3_cache_file
        )

        """
        # make sure cache file exists
        if not os.path.exists(cache_path):
            print("Need to generate Spotify API token first. Run setup_spotify.py.", file=sys.stderr)
            sys.exit(1)
        """

        self.wrapper     = spotipy.Spotify(oauth_manager=oauth_manager)
        self.top_artists = []
        self.top_tracks  = []

    def refresh(self):
        try:
            self.top_artists = self._top_artists()
            self.top_tracks = self._top_tracks()
        except requests.exceptions.ConnectionError:
            pass

    def _top_artists(self):
        return self.wrapper.current_user_top_artists(limit=self.TOP_LIMIT, time_range="short_term")

    def _top_tracks(self):
        return self.wrapper.current_user_top_tracks(limit=self.TOP_LIMIT, time_range="short_term")


class SpotifyOAuthWithS3Cache(WaitingForPyPiUpdateSpotifyOAuth):
    def __init__(self, s3_bucket, s3_cache_file, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.s3_client = boto3.client("s3")
        self.s3_bucket = s3_bucket
        self.s3_cache_file = s3_cache_file

    def get_cached_token(self):
        # pull from S3 to local file
        self.s3_client.download_file(self.s3_bucket, self.s3_cache_file, self.cache_path)

        with open(self.cache_path) as f:
            token_info_string = f.read()

        token_info = json.loads(token_info_string)

        if self.is_token_expired(token_info):
            token_info = self.refresh_access_token(
                token_info["refresh_token"]
            )

        return token_info

    def _save_token_info(self, token_info):
        # save to local file
        f = open(self.cache_path, "w+")
        f.write(json.dumps(token_info))
        f.close()

        # copy file to S3
        self.s3_client.upload_file(self.cache_path, self.s3_bucket, self.s3_cache_file)


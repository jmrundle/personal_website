import time
import json
import requests
import spotipy
import boto3
from .oauth2 import SpotifyOAuth


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
            scopes=app.config["SPOTIFY_SCOPES"],
            s3_bucket=app.config["S3_BUCKET"],
            s3_cache_file=app.config["S3_CACHE_FILE"]
        )

        self.services       = [self.spotify, self.github]
        self.refresh_period = int(app.config["API_REFRESH_PERIOD"])
        self.last_refresh   = 0
        self.refresh()

    def refresh(self):
        # TODO: do this in background, not attatched to any requests
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

    def __init__(self, client_id, client_secret, redirect_uri, scopes, s3_bucket, s3_cache_file):
        oauth_manager = SpotifyOAuthWithS3Cache(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes,
            s3_bucket_name=s3_bucket,
            s3_cache_file=s3_cache_file
        )

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


# overwrite base SpotifyOAuth Class to support S3 cache storage
class SpotifyOAuthWithS3Cache(SpotifyOAuth):
    def __init__(self, s3_bucket_name, s3_cache_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s3          = boto3.resource("s3")
        s3_bucket   = s3.Bucket(s3_bucket_name)
        self.s3_key = s3_bucket.Object(key=s3_cache_file)

        self.cached_token = None

    def get_cached_token(self):
        if self.cached_token is not None:
            return self.cached_token

        # pull from S3
        data = self.s3_key.get()["Body"]
        token_info = json.load(data)

        if self.is_token_expired(token_info):
            token_info = self.refresh_access_token(
                token_info["refresh_token"]
            )

        # subsequent calls will return same object
        self.cached_token = token_info

        return token_info

    def _save_token_info(self, token_info):
        # update local cached token
        self.cached_token = token_info

        # push to s3
        # TODO: make this asynchronous
        data = json.dumps(token_info)
        self.s3_key.put(Body=data)

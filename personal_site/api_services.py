import requests
import spotipy
from .oauth2 import SpotifyOAuth

# import boto3


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
            cache_path=app.config["SPOTIFY_CACHE_PATH"]
        )


class Github:
    API_PREFIX = "https://api.github.com"
    EVENT_COUNT = 10

    def __init__(self, username, access_token):
        self.username     = username
        self.access_token = access_token
        self.profile      = self._profile()
        self.events       = self._events()

    def _request(self, url):
        headers = {
            "Authorization": f"{self.username}:{self.access_token}"
        }

        try:
            resp = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            return {}

        if not resp.ok:
            return {}

        return resp.json()

    def _profile(self):
        url = f"{self.API_PREFIX}/users/{self.username}"
        return self._request(url)

    def _events(self, event_count=EVENT_COUNT):
        url = f"{self.API_PREFIX}/users/{self.username}/events"
        requests.get(url)
        return self._request(url)[:event_count]


class Spotify:
    TOP_LIMIT = 8

    def __init__(self, client_id, client_secret, redirect_uri, scopes, cache_path):
        oauth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes,
            cache_path=cache_path
        )

        self.wrapper     = spotipy.Spotify(oauth_manager=oauth_manager)
        self.top_artists = self._top_artists()
        self.top_tracks  = self._top_tracks()

    def _top_artists(self, top_artists_limit=TOP_LIMIT):
        return self.wrapper.current_user_top_artists(limit=top_artists_limit, time_range="short_term")

    def _top_tracks(self, top_tracks_limit=TOP_LIMIT):
        return self.wrapper.current_user_top_tracks(limit=top_tracks_limit, time_range="short_term")


"""
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
"""

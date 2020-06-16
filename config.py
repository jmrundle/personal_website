import os
import dotenv
import yaml


class Social:
    def __init__(self, name, url_prefix, fa_icon, username, bg_col):
        self.name       = name
        self.url_prefix = url_prefix
        self.fa_icon    = fa_icon
        self.username   = username
        self.bg_col     = bg_col
        self.url        = url_prefix + username


def load_instance_info(info_path):
    info = yaml.load(open(info_path, 'r'), Loader=yaml.FullLoader)

    # associate username's with URL prefixes, icons, etc.
    social_config = yaml.load(open("social_config.yml", 'r'), Loader=yaml.FullLoader)
    social_objects = {}
    for platform in info["social_usernames"]:
        if platform not in social_config:
            continue
        config = social_config[platform]
        config["username"] = info["social_usernames"][platform]
        social_objects[platform] = Social(**config)

    info["social_objects"] = social_objects

    return info


class Config(object):
    # Flask related
    DEBUG   = False
    TESTING = False

    API_REFRESH_PERIOD = 1800  # seconds until we refresh API objects (30 min)

    # folder structure
    # instance
    #   |___ posts/
    #   |___ resources/
    #   |___ tmp/
    #   |___ .env
    #   |___ info.yml
    ENV_FILE      = ".env"
    INSTANCE_PATH = os.path.join(os.path.dirname(__file__), "instance")
    POSTS_PATH    = os.path.join(INSTANCE_PATH, "posts")
    RESOURCE_PATH = os.path.join(INSTANCE_PATH, "resources")
    TMP_PATH      = os.path.join(INSTANCE_PATH, "tmp")
    DATA_FILE     = os.path.join(INSTANCE_PATH, "info.yml")

    # load env variables from optional .env file
    #   - NOTE: default path is ./instance/.env
    if os.path.exists(ENV_FILE):
        dotenv.load_dotenv(ENV_FILE, verbose=True)

    # load secret keys into flask config object
    #   - raise exception if not set
    GITHUB_ACCESS_TOKEN   = os.environ.get('GITHUB_ACCESS_TOKEN')
    SPOTIFY_CLIENT_ID     = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI  = os.environ.get('SPOTIFY_REDIRECT_URI')
    SPOTIFY_CACHE_PATH    = os.path.join(TMP_PATH, ".spotify-cache")
    SPOTIFY_SCOPES        = "user-top-read"

    # information from info.yml
    INSTANCE_INFO  = load_instance_info(DATA_FILE)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

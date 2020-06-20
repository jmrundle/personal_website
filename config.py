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
    # .env
    # instance/
    #   |___ posts/
    #   |___ resources/
    #   |___ tmp/
    #   |___ info.yml
    ENV_FILE     = os.path.join(os.path.dirname(__file__), ".env")
    INSTANCE_DIR = os.path.join(os.path.dirname(__file__), "instance")
    POSTS_DIR    = os.path.join(INSTANCE_DIR, "posts")
    RESOURCE_DIR = os.path.join(INSTANCE_DIR, "resources")
    TMP_DIR      = os.path.join(INSTANCE_DIR, "tmp")
    DATA_FILE    = os.path.join(INSTANCE_DIR, "info.yml")

    # load env variables from optional .env file
    if os.path.exists(ENV_FILE):
        dotenv.load_dotenv(ENV_FILE, verbose=True)

    # load secret keys into flask config object
    #   - raise exception if not set
    GITHUB_ACCESS_TOKEN   = os.environ.get('GITHUB_ACCESS_TOKEN')
    SPOTIFY_CLIENT_ID     = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI  = os.environ.get('SPOTIFY_REDIRECT_URI')
    SPOTIFY_CACHE_PATH    = os.path.join(TMP_DIR, ".spotify-cache")
    SPOTIFY_SCOPES        = "user-top-read"

    AWS_ACCESS_KEY_ID     = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION    = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    S3_BUCKET             = os.environ.get("S3_BUCKET", "personal-site-storage")
    S3_CACHE_FILE         = ".spotify-cache"

    # information from info.yml
    INSTANCE_INFO  = load_instance_info(DATA_FILE)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

from dataclasses import dataclass
from functools import wraps


@dataclass
class Social:
    name: str
    url_prefix: str
    fa_icon: str
    username: str
    bg_col: str

    @property
    def url(self):
        return self.url_prefix + self.username


class NavigationLink:
    def __init__(self, endpoint, title):
        self.endpoint = endpoint
        self.title    = title


class Navigation:
    def __init__(self):
        self.active = None
        self._mapping  = dict()

    @property
    def links(self):
        return self._mapping.values()

    def is_active(self, link: NavigationLink):
        return link == self.active

    def register(self, endpoint: str, title: str):
        def wrapper(func):
            self._mapping[func] = NavigationLink(endpoint, title)

            @wraps(func)
            def wrapped(*endpoint_args, **endpoint_kw):
                self.active = self._mapping[func]
                return func(*endpoint_args, **endpoint_kw)

            return wrapped

        return wrapper

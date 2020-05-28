from functools import wraps


class Social:
    def __init__(self,
                 name,
                 url_prefix,
                 fa_icon,
                 username,
                 bg_col):
        self.name       = name
        self.url_prefix = url_prefix
        self.fa_icon    = fa_icon
        self.username   = username
        self.bg_col     = bg_col

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

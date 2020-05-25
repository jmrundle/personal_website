from dataclasses import dataclass
from flask import Flask


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


class Navigation:
    def __init__(self):
        self.links = []

    def route(self, name, endpoint):
        def decorator(f, *args, **kwargs):
            def wrapper(*args, **kwargs):
                self.links.append(
                    {
                        "name": name,
                        "endpoint": endpoint
                     }
                )
                f(*args, **kwargs)
            return wrapper(args, kwargs)

        return decorator

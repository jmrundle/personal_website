import jinja2
import datetime


def format_time(input_time: str):
    time = datetime.datetime.strptime(input_time, "%Y-%m-%dT%H:%M:%SZ")
    return datetime.datetime.strftime(time, "%m/%d/%Y")


def git_api_to_html(api_url: str):
    return api_url \
        .replace("api.github", "github") \
        .replace("/repos", "") \
        .replace("/users", "") \
        .replace("/commits", "/commit")


def css_classes(class_list: list):
    return " ".join(class_list)


jinja2.filters.FILTERS["format_time"] = format_time
jinja2.filters.FILTERS["git_api_to_html"] = git_api_to_html
jinja2.filters.FILTERS["css_classes"] = css_classes

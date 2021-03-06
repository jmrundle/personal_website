import glob
import markdown2
import frontmatter
import os.path
import datetime


class InvalidPostException(BaseException):
    pass


class Post:
    def __init__(self, metadata, html, creation_ts):
        self.endpoint = ""
        self.metadata = metadata
        self.html = html
        self.creation_ts = creation_ts

    def has_valid_metadata(self):
        return self.metadata.get("title", None) is not None and \
            self.metadata.get("description", None) is not None and \
            self.metadata.get("image", None) is not None and \
            self.metadata.get("tags", None) is not None

    def insert_into(self, posts):
        # make post name URL safe

        #  use title, strip whitespace and replace with spaces
        name = self.metadata.get("title")
        name = '-'.join(name.lower().split())

        #  add numbers to make unique if necessary
        suffix = ""
        num = 1
        while (name + suffix) in posts:
            num += 1
            suffix = '-' + str(num)

        self.endpoint = name + suffix
        posts[self.endpoint] = self


def load_posts(post_path, file_extension="md"):
    # fetch all markdown file names
    filenames = glob.glob(os.path.join(post_path, "*." + file_extension))

    # structure like:
    #   {
    #       post_endpoint: Post (object)
    #   }
    posts = dict()

    for filename in filenames:
        with open(filename, 'r') as markdown_file:
            data = frontmatter.load(markdown_file)

            html = markdown2.markdown(data.content, extras=["fenced-code-blocks"])

            creation_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
            creation_ts = creation_datetime.strftime("%b %-d, %Y")

            post = Post(data.metadata, html, creation_ts)

        if not post.has_valid_metadata():
            raise InvalidPostException

        post.insert_into(posts)

    return posts


def is_subset(needle, haystack):
    if not isinstance(needle, set):
        needle = set(needle)
    return needle.issubset(haystack)


if __name__ == "__main__":
    load_posts("../instance/posts")
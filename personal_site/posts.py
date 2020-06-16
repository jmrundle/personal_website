import glob
import frontmatter
import os.path


class InvalidPostException(BaseException):
    pass


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
            metadata = frontmatter.load(markdown_file)

        # make sure each post has the
        if metadata.get("title", None) is None or \
                metadata.get("description", None) is None or \
                metadata.get("image", None) is None or \
                metadata.get("tags", None) is None:
            raise InvalidPostException

        # make post name URL safe

        #  use title, strip whitespace and replace with spaces
        name = metadata.get("title")
        name = '-'.join(name.lower().split())

        #  add numbers to make unique if necessary
        suffix = ""
        num = 1
        while (name + suffix) in posts:
            num += 1
            suffix = '-' + str(num)

        posts[name + suffix] = metadata

    return posts


def is_subset(needle, haystack):
    if not isinstance(needle, set):
        needle = set(needle)
    return needle.issubset(haystack)

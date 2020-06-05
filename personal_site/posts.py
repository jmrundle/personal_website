import glob
import frontmatter
import os.path


def load_posts(post_path, file_extension="md"):
    # fetch all markdown file names
    filenames = glob.glob(os.path.join(post_path, "*." + file_extension))

    # structure like:
    #   {
    #       post_name: Post (object)
    #   }
    posts = dict()

    for filename in filenames:
        with open(filename, 'r') as markdown_file:
            metadata = frontmatter.load(markdown_file)

        # make post name URL safe
        #  - take filename on server, extract extension
        #  - strip whitespace and replace with spaces
        name = str(os.path.splitext(os.path.basename(filename))[0])
        name = '-'.join(name.lower().split())

        posts[name] = metadata

    return posts

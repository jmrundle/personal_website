import glob
import frontmatter
import os.path


def load_posts(post_path, file_extension="md"):
    # fetch all markdown file names
    files = glob.glob(os.path.join(post_path, "*." + file_extension))

    # structure like:
    #   {
    #       post_name: Post (object)
    #   }
    posts = dict()

    for filename in files:
        with open(filename, 'r') as markdown_file:
            metadata = frontmatter.load(markdown_file)

        # make post name URL safe
        #  - take filename on server, extract extension
        #    strip whitespace and replace spaces
        name = str(os.path.splitext(os.path.basename(filename))[0])
        name = name.strip().lower().replace(' ', '-')

        posts[name] = metadata

    return posts

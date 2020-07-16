import os.path
from flask import render_template, send_from_directory, abort, request
from flask_caching import Cache
import markdown
import markdown.extensions.codehilite
from .api_services import ApiServices
from .navigation import Navigation
from .posts import load_posts, is_subset


def register_routes(app):
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    refresh_period = int(app.config["API_REFRESH_PERIOD"])

    # load these once
    nav = Navigation()
    posts = load_posts(app.config["POSTS_DIR"])
    resume = app.config["INSTANCE_INFO"]["resume"]

    # inject these global variables into each template
    #   - as convention, use the 'g_' prefix for each
    @app.context_processor
    def base_template():
        config = app.config["INSTANCE_INFO"]
        return dict(
            g_navigation = nav,
            g_name = config["name"],
            g_description = config["description"],
            g_avatar = config["avatar"],
            g_socials = config["social_objects"]
        )

    @app.route("/", methods=["GET"])
    @nav.register("/", "Home")
    def index():
        return render_template("index.html", about=app.config["INSTANCE_INFO"]["about"])

    @app.route("/more", methods=["GET"])
    @nav.register("/more", "More")
    @cache.cached(timeout=refresh_period)
    def more():
        api_services = ApiServices(app)

        return render_template("more.html", apis=api_services)

    @app.route("/resume", methods=["GET"])
    @nav.register("/resume", "Resume")
    def projects():
        return render_template("resume.html", resume=resume)

    @app.route("/posts", methods=["GET"])
    @nav.register("/posts", "Posts")
    def post_listing():
        tags = request.args.get("tags", None)
        if tags is None:
            tags = set()
        else:
            tags = set(tags.split(','))

        post_data = []
        for endpoint, metadata in posts.items():
            if tags and not is_subset(tags, metadata["tags"]):
                continue

            post_data.append((endpoint, metadata))

        return render_template("post_listing.html", post_data=post_data, tags=tags)

    @app.route("/posts/<name>", methods=["GET"])
    def post(name):
        text = posts.get(name, None)
        if text is None:
            return abort(404)

        html = markdown.markdown(text.content, extensions=["codehilite"])
        return render_template("post.html", post_content=html)

    @app.route('/resources/<path:filename>', methods=["GET"])
    def serve(filename):
        if not os.path.exists(os.path.join(app.config["RESOURCE_DIR"], filename)):
            return abort(404)

        return send_from_directory(app.config["RESOURCE_DIR"], filename)

    @app.route('/favicon.ico', methods=["GET"])
    def favicon():
        return serve('favicon.ico')

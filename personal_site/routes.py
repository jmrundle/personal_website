from flask import render_template, send_from_directory, abort
import markdown
from .api_services import ApiServices
from .models import Navigation
from .posts import load_posts


def register_routes(app):
    # load these once
    apis   = ApiServices(app.config)
    nav    = Navigation()
    posts  = load_posts(app.config["POSTS_PATH"])
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
        return render_template("index.html")

    # @cache
    @app.route("/more", methods=["GET"])
    @nav.register("/more", "More")
    def more():
        apis.refresh()
        return render_template("more.html", apis=apis)

    @app.route("/resume", methods=["GET"])
    @nav.register("/resume", "Resume")
    def projects():
        return render_template("resume.html", resume=resume)

    @app.route("/posts", methods=["GET"])
    @nav.register("/posts", "Posts")
    def test():
        return render_template("post_listing.html", posts=posts)

    @app.route("/posts/<name>", methods=["GET"])
    def get_post(name):
        text = posts.get(name, None)
        if text is None:
            return abort(404)

        html = markdown.markdown(text.content, extensions=["codehilite"])
        return render_template("post.html", post_content=html)

    @app.route('/resources/<path:filename>', methods=["GET"])
    def serve(filename):
        return send_from_directory(app.config["RESOURCE_PATH"], filename)

    @app.route('/favicon.ico', methods=["GET"])
    def favicon():
        return serve('favicon.ico')

    return app

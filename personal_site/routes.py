from flask import render_template, send_from_directory
from .api_services import ApiServices
from .models import Navigation


def register_routes(app):
    # load these once
    apis = ApiServices(app)

    # inject these global variables into each template
    #   - as convention, we use the 'g_' prefix for each
    @app.context_processor
    def base_template():
        config = app.config["INSTANCE_INFO"]
        return dict(
            g_navigation = [],
            g_name = config["name"],
            g_description = config["description"],
            g_avatar = config["avatar"],
            g_socials = config["social_objects"]
        )

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    # @cache
    @app.route("/more", methods=["GET"])
    def more():
        apis.refresh()
        return render_template("more.html", apis=apis)

    @app.route("/projects", methods=["GET"])
    def projects():
        return render_template("base.html")

    @app.route("/test", methods=["GET"])
    def test():
        return render_template("base.html")

    @app.route('/resources/<path:filename>', methods=["GET"])
    def serve(filename):
        return send_from_directory(app.config["MEDIA_PATH"], filename)

    @app.route('/favicon.ico', methods=["GET"])
    def favicon():
        return serve('favicon.ico')

    return app

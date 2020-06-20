def build_app(*args, **kwargs):
    from flask import Flask
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # register jinja2 filters
    from personal_site import filters

    app.config.from_object("config.ProductionConfig")

    from personal_site import routes
    routes.register_routes(app)

    return app

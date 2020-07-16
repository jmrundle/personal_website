def build_app(debug=False, *args, **kwargs):
    from flask import Flask
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # register jinja2 filters
    from personal_site import filters

    # load config
    if debug:
        app.config.from_object("config.app_config.Development")
    else:
        app.config.from_object("config.app_config.Production")

    from personal_site import routes
    routes.register_routes(app)

    return app

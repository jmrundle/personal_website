from flask import Flask

app = Flask(__name__, template_folder="templates", static_folder="static")

# -------- register jinja2 filters -------------------
from personal_site import filters


# -------- config - one public, another secret -------
app.config.from_object("config.DevelopmentConfig")


# -------- register routes for app -------------------
from personal_site import routes
app = routes.register_routes(app)

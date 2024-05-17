import pathlib
import connexion, connexion.options as SwaggerOptions
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, sys, json

config_file = "config_dev.json"
db_config = {}

if os.getenv("BOT_LIVE") == "1":
    config_file = "config.json"
else:
    print("BOT_LIVE environment variable not found or 0, developer mode on")
    
if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/{config_file}"):
    sys.exit(f"{config_file} not found! Exiting application...")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/{config_file}") as file:
        db_config = json.load(file)

basedir = pathlib.Path(__file__).parent.resolve()

options = SwaggerOptions.SwaggerUIOptions(swagger_ui=db_config.get("ENABLE_SWAGGER_UI"), serve_spec=db_config.get("ENABLE_SWAGGER_UI"))
connex_app = connexion.App(__name__, specification_dir=basedir, swagger_ui_options=options)

connection_string = f"{db_config.get('DB_ENGINE')}://{db_config.get('DB_USER')}:{db_config.get('DB_PASS')}@{db_config.get('DB_HOST')}:{db_config.get('DB_PORT')}/{db_config.get('DB_NAME')}"

print(connection_string)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
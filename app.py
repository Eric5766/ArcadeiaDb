import config
from models import User

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return "?"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

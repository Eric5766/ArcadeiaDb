from connexion.exceptions import OAuthProblem
from config import db_config

key = db_config.get("API_KEY")

def apikey_auth(token, required_scopes):
    if token and str(token)==key:
        return {"sub" : db_config.get("API_KEY")}
    else:
        raise OAuthProblem("Invalid token")
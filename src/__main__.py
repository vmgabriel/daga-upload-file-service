# develop vmgabriel

# Libraries
from flask import Flask, jsonify
from flask_jwt import JWT
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from src.config.server import configuration as conf

# Routes
from src.protocols.http.v0.index import mod
from src.protocols.http.v0.files import mod as fmodule

app = Flask(__name__, static_folder=conf['files_path_upload'])

app.config['JWT_TOKEN_LOCATION'] = conf['jwt_location']
app.config['JWT_SECRET_KEY'] = conf['jwt_secret']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

app.register_blueprint(mod, url_prefix='/api')
app.register_blueprint(fmodule, url_prefix='/api/uploads')

if __name__ == '__main__':
    app.run (
        host=conf['host'],
        debug=conf['debug'],
        port=conf['port']
    )


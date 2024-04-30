"""Launch the web application email scoring."""

import os

from flask import Flask

from core.api import urls_blueprint
from core.swagger_docs.swagger_config import SWAGGER_URL, swaggerui_blueprint

app = Flask(__name__, static_url_path="/static")
app.register_blueprint(urls_blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(
        host=os.environ.get("APP_INCOMING_CONNECTIONS", "127.0.0.1"),
        port=port,
        debug=False,
    )

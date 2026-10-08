from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from routes.security_routes import security_bp
from storage.database import initialize_database


app = Flask(__name__)

CORS(app)

app.register_blueprint(security_bp)


# Path to frontend folder
FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


# Serve frontend
@app.route("/")
def frontend():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# Serve CSS
@app.route("/style.css")
def stylesheet():
    return send_from_directory(
        FRONTEND_FOLDER,
        "style.css"
    )


# Serve JavaScript
@app.route("/script.js")
def javascript():
    return send_from_directory(
        FRONTEND_FOLDER,
        "script.js"
    )


@app.route("/api/health")
def health():
    return {
        "server": "Cloud Security Server",
        "status": "online"
    }


initialize_database()


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )
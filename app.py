from flask import Flask
from routes.alerts import alerts_bp
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging so errors are visible in console/logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")

# Register blueprints (route groups)
app.register_blueprint(alerts_bp)


@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404


@app.errorhandler(405)
def method_not_allowed(e):
    return {"error": "Method not allowed"}, 405


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")

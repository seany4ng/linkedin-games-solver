from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env
    load_dotenv('../.env')  # Adjust the path based on your project structure

    app = Flask(__name__)
    CORS(app)

    # Load config variables from environment
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['HOST'] = os.getenv('FLASK_RUN_HOST', 'localhost')
    app.config['PORT'] = os.getenv('FLASK_RUN_PORT', '8000')

    from .routes import tango_solve
    app.register_blueprint(tango_solve, url_prefix="/tango")

    from .routes import queens_solve
    app.register_blueprint(queens_solve, url_prefix="/queens")

    return app

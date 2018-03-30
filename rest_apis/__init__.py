from flask import Flask
from flask_socketio import SocketIO, send
from flask_cors import CORS
from multiprocessing import Process
import os

FlaskApp = Flask(__name__)
"""
The flask application.
"""
FlaskApp.config['SECRET_KEY'] = 'secret!'

BASE_URL = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CLIENT_APP_FOLDER = os.path.join(BASE_URL, "client-app")

print(CLIENT_APP_FOLDER)


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

cors = CORS(FlaskApp, resources={r"/api/*": {"origins": "*"}})


class FlaskAppLauncher(Process):
    """
    A class that starts a Flask HTTP server. The Flask server allows us to create GET/POST API services and bind them to
    URLs.
    """

    def __init__(self):
        self.app = FlaskApp
        super().__init__()

    def run(self):
        """
        Overrides the Process run method and starts a Flask server.
        """
        port = int(os.environ.get('PORT', 5000))
        self.app.run(host='0.0.0.0', port=port)

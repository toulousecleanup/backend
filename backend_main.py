"""
This is the Backend entry point. Its role is to:

    * start the DataReceiver() to receive and store in Database the HTTP POST messages from SigFox callback.
"""
from rest_apis import FlaskAppLauncher
from rest_apis.data_receiver_api import DataReceiver
from rest_apis.database_reader_api import DatabaseReader
from rest_apis.mail_list_manager_api import MailListManager

#sigfox IP -  185.110.97.11


if __name__ == '__main__':
    # Start Flask app
    flask_launcher = FlaskAppLauncher()
    flask_launcher.start()
    # Instantiate DataReceiver and DatabaseReader
    DataReceiver()
    MailListManager()
    DatabaseReader()


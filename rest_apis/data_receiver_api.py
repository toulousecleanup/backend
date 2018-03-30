from flask import request, jsonify
from flask_mail import Mail, Message
import datetime

from database.database import SigFoxMessages, LatestSigFoxMessages, AlarmsMailList, Session
from . import FlaskApp

FlaskApp.config['MAIL_SERVER']='smtp.gmail.com'
FlaskApp.config['MAIL_PORT'] = 587
FlaskApp.config['MAIL_USERNAME'] = '' # your mail server here
FlaskApp.config['MAIL_PASSWORD'] = '' # your password hgere
FlaskApp.config['MAIL_USE_TLS'] = True
FlaskApp.config['MAIL_USE_SSL'] = False
mail = Mail(FlaskApp)


class DataReceiver():
    """
    A class that handles the reception of SigFox backend HTTP POST messages. It extracts the data contained in the JSON
    payload of the HTTP POST and appends it to the database table 'sigfox_messages'.
    """
    def __init__(self):
        self.app = FlaskApp

    @FlaskApp.route('/api/callback_handler/<device_id>', methods=['POST'])
    def callback_handler(device_id):
        """
        Receives the json formatted callback message from a given sigfox device.
        It stores the information into the database.

        Args:
             device_id (str): the SigFox device id that has triggered the callback

        Returns:
            json: The device_id as a response with HTTP 200 OK.
        """
        json_msg = request.json
        date_time = str(datetime.datetime.now().strftime("%d %B %Y    -     %X")).split(".")[0]
        print(date_time)

        db_session = Session()

        # Append message to 'sigfox_messages' table
        db_msg = SigFoxMessages()
        db_msg.device_id = json_msg["device_id"]
        db_msg.date = date_time
        db_msg.level = json_msg["level"]
        db_session.add(db_msg)

        # Create 'latest_sigfox_messages' table entry or update it if existing for the current device_id
        if db_session.query(LatestSigFoxMessages).filter(LatestSigFoxMessages.device_id == device_id).count() == 0:
            latest_db_msg = LatestSigFoxMessages()
            latest_db_msg.device_id = json_msg["device_id"]
            latest_db_msg.date = date_time
            latest_db_msg.level = json_msg["level"]
            db_session.add(latest_db_msg)
        else:
            entry_to_update = db_session.query(LatestSigFoxMessages).filter(LatestSigFoxMessages.device_id ==
                                                                            device_id).one()
            entry_to_update.date = date_time
            entry_to_update.level = json_msg["level"]

        db_session.commit()
        db_session.close()

        # Send mail if necessary
        if json_msg["level"] >= 75:
            recipients = get_mail_list()
            if recipients != []:
                msg = Message('Alerte bac plein', sender='toulousecleanup@gmail.com',
                              recipients=recipients)
                msg.body = "Salut, il est temps d'aller vider le bac {} qui est plein à {} %".format(json_msg["device_id"],
                                                                                                     json_msg["level"])
                mail.send(msg)

        # send 200 OK to SigFox backend
        return jsonify({"device_id": device_id})


def get_mail_list():
    db_session = Session()
    qryresult = db_session.query(AlarmsMailList).all()

    mail_list = list(i.mail_address for i in qryresult)
    db_session.close()
    return mail_list
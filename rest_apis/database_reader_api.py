from flask import jsonify

from database.database import LatestSigFoxMessages, SigFoxMessages, AlarmsMailList, Session
from . import FlaskApp


class DatabaseReader():
    """
        A class to access data from our Database from a remote machine. It implement HTTP rest API services.
    """
    def __init__(self):
        self.app = FlaskApp

    @FlaskApp.route('/api/get_sigfox_messages', methods=['GET'])
    def get_sigfox_messages():
        """
        Returns a 200 OK with the 'sigfox_messages' table content (JSON formatted)

        Returns:
            json: A json representation of the content of table sigfox_messages with HTTP 200 OK.
        """
        db_session = Session()
        qryresult = db_session.query(SigFoxMessages).all()

        resp_json = jsonify(json_list=[i.serialize for i in qryresult])
        db_session.close()

        return resp_json

    @FlaskApp.route('/api/get_sigfox_messages/latest/weight/<device_id>', methods=['GET'])
    def get_latest_weight(device_id):
        """
        Returns a HTTP 200 OK with the latest weight for the given device (JSON formatted)

        Returns:
            json: A json representation of the latest device stored weight with HTTP 200 OK.
        """
        db_session = Session()
        qryresult = db_session.query(LatestSigFoxMessages).filter(LatestSigFoxMessages.device_id == device_id).one()
        level = qryresult.level;

        resp_json = jsonify({"level": level})
        db_session.close()

        return resp_json

    @FlaskApp.route('/api/get_sigfox_messages/latest', methods=['GET'])
    def get_latest_sigfox_messages():
        """
        Returns a 200 OK with the 'latest_sigfox_messages' table content (JSON formatted)

        Returns:
            json: A json representation of the content of table sigfox_messages with HTTP 200 OK.
        """
        db_session = Session()
        qryresult = db_session.query(LatestSigFoxMessages).all()

        resp_json = jsonify(json_list=[i.serialize for i in qryresult])
        db_session.close()

        return resp_json

    @FlaskApp.route('/api/get_sigfox_messages/all/<device_id>', methods=['GET'])
    def get_sigfox_messages_for_device(device_id):
        """
        Returns a 200 OK with the 'sigfox_messages' table content for a given device (JSON formatted)

        Args:
             device_id (str): the SigFox device id that has triggered the callback

        Returns:
            json: A json representation of the content of table sigfox_messages (for one device) with HTTP 200 OK.
        """
        db_session = Session()
        qryresult = db_session.query(SigFoxMessages).filter(SigFoxMessages.device_id == device_id)

        resp_json = jsonify(json_list=[i.serialize for i in qryresult])
        db_session.close()

        return resp_json

    @FlaskApp.route('/api/get_alarms_mail_list', methods=['GET'])
    def get_alarms_mail_list():
        """
        Returns a 200 OK with the 'alarms_mail_list' table content (JSON formatted)

        Returns:
            json: A json representation of the content of tablealarms_mail_list (for one device) with HTTP 200 OK.
        """
        db_session = Session()
        qryresult = db_session.query(AlarmsMailList).all()

        resp_json = jsonify(json_list=[i.serialize for i in qryresult])
        db_session.close()

        return resp_json

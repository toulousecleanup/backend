from flask import request, jsonify

from database.database import AlarmsMailList, Session
from . import FlaskApp


class MailListManager():
    """
    A class that updates the mailing list for alerts.
    """
    @FlaskApp.route('/api/add_contact', methods=['POST'])
    def new_contact_handler():
        """
        Receives the json formatted new contact (first_name, last_name, mail_address).
        It stores the information into the database.

        Returns:
            json: HTTP 200 OK.
        """
        json_msg = request.json
        mail_address = json_msg["mail_address"]
        print(mail_address)

        db_session = Session()

        # Create 'latest_sigfox_messages' table entry or update it if existing for the current device_id
        if db_session.query(AlarmsMailList).filter(AlarmsMailList.mail_address == mail_address).count() == 0:
            new_contact = AlarmsMailList()
            new_contact.mail_address = mail_address
            new_contact.first_name = json_msg["first_name"]
            new_contact.last_name = json_msg["last_name"]

            db_session.add(new_contact)

        else:
            print("email already registered")

        db_session.commit()
        db_session.close()

        # send 200 OK
        return jsonify({"mail_address": mail_address})

    @FlaskApp.route('/api/delete_contact/<mail>', methods=['DELETE'])
    def delete_contact(mail):
        """
        Deletes the contact information that matches the mail argument.

        Args:
            mail(string): the mail address of the contact to delete from mail list

        Returns:
            json: HTTP 200 OK.
        """
        db_session = Session()
        print(str(mail))

        # delete database entry that matches the parameter 'mail'
        query = db_session.query(AlarmsMailList).filter(AlarmsMailList.mail_address == str(mail))

        # Check unicity of entry and delete it
        if query.count() != 0:
            to_delete = query.one()
            db_session.delete(to_delete)

        db_session.commit()
        db_session.close()

        # send 200 OK
        return jsonify({"mail_address": mail})

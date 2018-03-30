# backend
The Flask backend server with database and mail manager

This code provides a simple Flask backend server to handle a few HTTP GET / POST requests to push / get new entries about a fluvial waste collector garbage tank level.
This way we can query these APIs to get the waste colector status.
There are also APIs to handle a mail list.

This backend also sends mails to the mail list addresses when the tank level is > 75%.

A demo of the backend can be found live at:

http://toulousecleanup.pythonanywhere.com/api/get_alarms_mail_list
http://toulousecleanup.pythonanywhere.com/api/get_sigfox_messages

among others

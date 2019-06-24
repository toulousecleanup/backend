Toulousecleanup website Backend
===============================

The Flask backend server with database and mail manager

This code provides a simple Flask backend server to handle a few HTTP GET / POST requests to push / get new entries about a fluvial waste collector garbage tank level.
This way we can query these APIs to get the waste colector status.
There are also APIs to handle a mail list.

This backend also sends mails to the mail list addresses when the tank level is > 75%.

A demo of the backend can be found live at:

http://toulousecleanup.pythonanywhere.com/api/get_alarms_mail_list
http://toulousecleanup.pythonanywhere.com/api/get_sigfox_messages

among others

Important note
--------------

The backend listens for HTTP POST on http://toulousecleanup.pythonanywhere.com/api/callback_handler/{device} (device is the SigFox device ID).

The HTTP POST payload expected to be:
```
{
  "device_id":"{device}", #0xFFFFFF format
  "seq_num":{seqNumber}, # uint8
  "level":{customData#level}  # The level from SigFox MKRFox1200 payload (uint8)
}
```
This mean you can connect any kind of device that respect this format (or even test via a REST client) and the website will work.


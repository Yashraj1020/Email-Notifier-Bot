import requests
import imaplib
import time
import email
from confidentials import Chat_id, bot_token, app_password 
def sendMessage(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data = {"chat_id": Chat_id, "text": message})
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login("yrajbhar669@gmail.com",  app_password)
imap.select("INBOX")
imap.noop()
status, messages = imap.search(None, "UNSEEN")
email_ids = messages[0].split()
if email_ids:
    last_seen = email_ids[-1]
else:
    last_seen = b"0"
print("Last seen:", last_seen)
while True:
    time.sleep(5)
    print("checking...")
    imap.noop()
    status, messages = imap.search(None, "UNSEEN")
    email_ids = messages[0].split()
    latest_message = email_ids[-1]
    print("Latest Message: ", latest_message)
    if int(latest_message) > int(last_seen):
        status, data = imap.fetch(latest_message, "(RFC822)")
        raw_email = None
        for item in data:
            if isinstance(item, tuple):
                raw_email = item[1]
                break
        if raw_email == None:
            continue
        Mail = email.message_from_bytes(raw_email)
        # print(Mail.keys())
        message =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\nSubject:{Mail['Subject']}\nReceived:{Mail.get('Date', 'Unkown')}\nMessage id: {Mail.get('Message-ID', "Unkown")}"
        sendMessage(message)
        last_seen = latest_message
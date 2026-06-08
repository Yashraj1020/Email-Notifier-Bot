import requests
import imaplib
import time
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from confidentials import Chat_id, bot_token, app_password 

def sendMessage(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, data = {"chat_id": Chat_id, "text": message})

def fetch_email_IDS():
    imap.noop()
    status, messages = imap.search(None, "ALL")
    return messages[0].split()

def get_email(latest_message):
    status, data = imap.fetch(latest_message, "(RFC822)")
    raw_email = None
    for item in data:
        if isinstance(item, tuple):
            raw_email = item[1]
            break
    if raw_email == None:
        return None
    mail = email.message_from_bytes(raw_email)
    return mail

def format_message(Mail, text):
    header = decode_header(Mail['Subject'])[0][0]
    if isinstance(header, bytes):
            subject = header.decode("utf-8")
    else:
        subject = header
    message =  f"📧 NEW EMAIL👤\n\n Sender:{Mail.get('From', 'Unkown')}\n\nSubject:{subject}\n\nReceived:{Mail.get('Date', 'Unkown')}\n\n Body:\n{text}\n ______________"
    return message

def extract_body(Mail):
    content_type = Mail.get_content_type()
    if content_type == "text/plain":
        return Mail.get_payload()
    elif content_type == "multipart/alternative" or content_type == "multipart/mixed":
        for part in Mail.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload()
            elif part.get_content_type == "text/html":
                html = part.get_payload()
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text(part)

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login("yrajbhar669@gmail.com",  app_password)
imap.select("INBOX")

email_ids = fetch_email_IDS()
if email_ids:
    last_seen = email_ids[-1]
else:
    last_seen = b"0"
print("Last seen:", last_seen)
while True:
    time.sleep(5)
    print("checking...")
    email_ids = fetch_email_IDS()
    if last_seen == b"0":
        last_seen = email_ids[-1]
    last_index = email_ids.index(last_seen)
    latest_messages = email_ids[last_index + 1 :]
    
    print("Latest Message/s: ", latest_messages)
    for latest_message in latest_messages:
        Mail = get_email(latest_message)
        if Mail is None:
            continue
        # print(Mail.keys())
        text = extract_body(Mail)
        message = format_message(Mail, text)
        sendMessage(message)
        last_seen = latest_message
        # print(Mail.get_content_type())
        # print(Mail.is_multipart)